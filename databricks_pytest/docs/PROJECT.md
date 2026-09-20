# Orders ETL Pipeline

A PySpark ETL pipeline that cleans, enriches, and aggregates order data, joining it
against customer data to produce per-order and per-customer outputs. Orders are
always ingested via Databricks Auto Loader from a Unity Catalog Volume — there is no
alternative (e.g. plain CSV) orders-loading path. It runs as a Databricks Job via a
notebook task, writing CSV/Delta on Unity Catalog Volumes.

## Project layout

```
.
├── src/
│   ├── pipeline.py          # entry point: CLI args, Spark session, orchestration, Auto Loader ingestion
│   ├── transformations.py   # reusable PySpark transformation functions
│   ├── schemas.py           # explicit StructType schemas for orders/customers CSVs
│   ├── orders_etl_notebook.py  # Databricks notebook entry point for the real pipeline job
│   └── run_tests_notebook.py   # Databricks notebook entry point that runs pytest on-cluster
├── tests/
│   ├── conftest.py          # session-scoped SparkSession + shared fixtures
│   ├── test_transformations.py  # unit tests per transformation function
│   └── test_pipeline.py     # integration tests for the full pipeline
├── data/
│   ├── orders.csv           # sample orders data for seeding the Auto Loader Volume (see DATABRICKS.md)
│   └── customers.csv        # sample customers data
├── resources/
│   ├── orders_etl_job.yml       # Databricks Asset Bundle job definition (real pipeline)
│   └── orders_etl_test_job.yml  # Databricks Asset Bundle job definition (pytest on-cluster)
├── databricks.yml           # Databricks Asset Bundle root config (target: dev)
├── pyproject.toml           # package metadata, dependencies, console entry point
└── pytest.ini                # pytest configuration
```

## How the pipeline works

Entry point: [src/pipeline.py](src/pipeline.py)

1. **Read** orders and customers with explicit schemas
   ([src/schemas.py](src/schemas.py)) — no schema inference. Both are ingested
   exclusively via Databricks Auto Loader (`cloudFiles`), each into their own
   Bronze Delta table, using `trigger(availableNow=True)` so each job run
   processes whatever new files have arrived and then exits, rather than
   running as a continuous stream. There is no CSV/batch fallback for either:
   - **Orders** — landed append-only into `orders_bronze_path` from
     `orders_input_path`, checkpointed at `orders_checkpoint_path`
     (`ingest_orders_autoloader`). The Bronze table is read back as an ordinary
     batch DataFrame — `deduplicate_orders`'s window function and the revenue
     aggregation need full-dataset batch semantics that structured streaming
     doesn't support.
   - **Customers** — landed into `customers_bronze_path` from
     `customers_input_path`, checkpointed at `customers_checkpoint_path`
     (`ingest_customers_autoloader`). Unlike orders, each micro-batch is
     **merged/upserted** on `customer_id` (SCD-Type-1: `whenMatchedUpdateAll`
     + `whenNotMatchedInsertAll` via `DeltaTable.merge`) rather than appended,
     since a customer record can be updated in place. The very first run
     bootstraps the Bronze table with a plain write, since `MERGE` needs an
     existing Delta table as its target.
2. **Transform** (`build_enriched_orders`), applying steps in order:
   - `clean_orders` — drops rows with a null `order_id` or `customer_id`; trims and
     upper-cases `product`; coalesces missing `quantity`/`unit_price` to `0`/`0.0`.
   - `deduplicate_orders` — keeps only the most recent row per `order_id` (by
     `order_date`, via a `ROW_NUMBER()` window function).
   - `add_order_total` — adds `total_amount = round(quantity * unit_price, 2)`.
   - `categorize_orders` — buckets `order_category` into `HIGH` (≥500), `MEDIUM`
     (≥100), or `LOW`.
   - `join_customer_region` — left-joins in `customer_name` and `region` from
     customers.
3. **Aggregate** (`aggregate_revenue_by_customer`) — sums `total_amount` and counts
   orders per `customer_id`.
4. **Write** both `enriched_orders` and `revenue_by_customer` to `{output_path}/...`,
   in the chosen format (`parquet` by default, or `delta`).

All transformation functions live in [src/transformations.py](src/transformations.py)
and are pure `DataFrame -> DataFrame` functions, independently unit-tested. There's
also a `filter_high_value_customers(agg_df, threshold)` helper (not currently wired
into `run_pipeline`, but covered by tests) for filtering the aggregated output.

`run_pipeline` has no CLI wrapper — it's only ever invoked from
[src/orders_etl_notebook.py](src/orders_etl_notebook.py), which sources its args from
`dbutils.widgets`. `get_spark_session()` uses `SparkSession.builder.getOrCreate()`, so
locally it creates a new session, while on a Databricks cluster it attaches to the
runtime's existing one.

## Data model

**orders.csv** ([data/orders.csv](data/orders.csv)) — schema `ORDERS_SCHEMA`:

| column        | type      | notes                        |
|---------------|-----------|-------------------------------|
| order_id      | string    | required                      |
| customer_id   | string    | required                      |
| product       | string    | nullable, normalized on read  |
| quantity      | integer   | nullable, coalesced to 0      |
| unit_price    | double    | nullable, coalesced to 0.0    |
| order_date    | timestamp | nullable, used for dedup order|

**customers.csv** ([data/customers.csv](data/customers.csv)) — schema `CUSTOMERS_SCHEMA`:

| column         | type   | notes    |
|----------------|--------|----------|
| customer_id    | string | required |
| customer_name  | string | nullable |
| region         | string | nullable |

## Testing

- Framework: `pytest` + `chispa` (DataFrame equality assertions for Spark).
- Config: [pytest.ini](pytest.ini) — tests live in `tests/`, discovered via
  `test_*.py` / `Test*` / `test_*`.
- [tests/conftest.py](tests/conftest.py) provides:
  - `spark` — a session-scoped `SparkSession`, 2 shuffle partitions. Reuses whatever
    session the Databricks runtime already provides (Spark Connect on serverless,
    classic Spark on a job cluster) rather than forcing a local master.
  - `raw_orders_df` — deliberately messy sample data (duplicate `order_id`, a null
    `order_id`, mixed-case product names, missing quantity/price) to exercise cleaning
    logic.
  - `customers_df` — small customers sample.
- [tests/test_transformations.py](tests/test_transformations.py) — one test per
  transformation function (clean, dedupe, total, categorize, join, aggregate, filter).
- [tests/test_pipeline.py](tests/test_pipeline.py) — end-to-end tests: full
  `build_enriched_orders` chain, and a `transform_and_write` run (in-memory
  DataFrames in, Parquet written to a temp dir and read back to assert on).

Tests only exercise in-memory fixtures via `build_enriched_orders`/`transform_and_write`
— never `run_pipeline`'s Auto Loader ingestion (orders or customers) itself, which
needs a real Databricks cluster and cloud storage to mean anything. There is no
CSV/batch loading path to fall back to for testing either.

Tests run on a Databricks cluster via
[resources/orders_etl_test_job.yml](resources/orders_etl_test_job.yml) /
[src/run_tests_notebook.py](src/run_tests_notebook.py), which installs `pytest` +
`chispa` on-cluster (Spark/Java are already provided by the runtime) and runs the
`tests/` directory:

```bash
databricks bundle run orders_etl_test_job -t dev
```

See [DATABRICKS.md](DATABRICKS.md) for the deploy/run commands.

## Packaging & dependencies

- [pyproject.toml](pyproject.toml) defines the `orders_etl` package (setuptools),
  Python ≥3.10, and runtime dependencies `pyspark==3.5.1` and `delta-spark==3.1.0`
  (needed for `DeltaTable.merge` in the customers upsert). Test dependencies
  (`pytest`, `chispa`) are installed on-cluster by
  [src/run_tests_notebook.py](src/run_tests_notebook.py), not via pyproject extras.
- No wheel is built or shipped for deployment — the Databricks job runs a notebook
  directly (see below).

## Databricks deployment (Asset Bundle)

The project deploys as a [Databricks Asset Bundle](https://docs.databricks.com/en/dev-tools/bundles/index.html).

- [databricks.yml](databricks.yml) — bundle root config:
  - Bundle name: `orders_etl`.
  - Includes job definitions from `resources/*.yml`.
  - Variables (overridable per target): `catalog` (default `kaninipro_catalog`), `schema` (default
    `orders_etl_dev`), and derived Unity Catalog Volume paths —
    `orders_input_path`/`orders_bronze_path`/`orders_checkpoint_path` for the
    append-only orders Auto Loader stream, `customers_input_path`/
    `customers_bronze_path`/`customers_checkpoint_path` for the merge/upsert
    customers Auto Loader stream, and `output_path` — all under
    `/Volumes/${var.catalog}/${var.schema}/...`.
  - Targets:
    - `dev` (default) — development mode.
  - The target has a placeholder `workspace.host` that must be set to the real
    Databricks workspace URL before deploying.

- [resources/orders_etl_job.yml](resources/orders_etl_job.yml) — defines the
  `orders_etl_job` Databricks Job (the real pipeline):
  - Job name: `orders-etl-${bundle.target}` (e.g. `orders-etl-dev`).
  - Runs on serverless compute — no `job_clusters` block and no
    `job_cluster_key` on the task, so there's no cluster to size or manage.
  - One task (`run_orders_etl`): a `notebook_task` pointing at
    [src/orders_etl_notebook.py](src/orders_etl_notebook.py), with `base_parameters`
    `orders_input_path`, `orders_bronze_path`, `orders_checkpoint_path`,
    `customers_input_path`, `customers_bronze_path`, `customers_checkpoint_path`,
    `output_path`, and `format: delta`.
  - [src/orders_etl_notebook.py](src/orders_etl_notebook.py) reads those parameters
    via `dbutils.widgets`, adds the synced repo root to `sys.path`, and calls
    `run_pipeline()` from [src/pipeline.py](src/pipeline.py) — the same code path
    used locally, so there's no separate packaging/build step to keep in sync.

- [resources/orders_etl_test_job.yml](resources/orders_etl_test_job.yml) — defines
  the `orders_etl_test_job` Databricks Job (runs the pytest suite on-cluster):
  - Job name: `orders-etl-tests-${bundle.target}`.
  - Also runs on serverless compute, same as the real pipeline job.
  - One task (`run_tests`): a `notebook_task` pointing at
    [src/run_tests_notebook.py](src/run_tests_notebook.py), which `%pip install`s
    `pytest`/`chispa` on-cluster and runs `pytest.main(["-v", "tests"])`, raising if
    any test fails (so a failed run shows as a failed Databricks job run). No
    `base_parameters` — it never touches ADLS/Auto Loader, only the sample data in
    `data/` and the fixtures in `tests/conftest.py`.

See [DATABRICKS.md](DATABRICKS.md) for deploy/run steps and prerequisites (catalog,
schema, volumes).

## Notes / things to be aware of

- `.gitignore` excludes `.databricks/` (local bundle state — e.g.
  `.databricks/bundle/dev/vscode.*.json` — is machine-generated and not tracked),
  standard Python/venv/pytest artifacts, and Spark warehouse/metastore files.
- The Databricks job always writes `delta` format; local CLI runs default to
  `parquet` unless `--format delta` is passed.
