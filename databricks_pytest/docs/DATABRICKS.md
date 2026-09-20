# Databricks Setup & Deployment

Steps to deploy this bundle and run its jobs, in order.

## 1. Bundle deployment

```bash
# set workspace.host in databricks.yml first (currently a placeholder)
databricks bundle validate -t dev
databricks bundle deploy -t dev
```

## 2. Create catalog + schema

Defaults from [databricks.yml](databricks.yml): catalog `kaninipro_catalog`, schema `orders_etl_dev`.

```sql
CREATE CATALOG IF NOT EXISTS kaninipro_catalog;
CREATE SCHEMA IF NOT EXISTS kaninipro_catalog.orders_etl_dev;
```

Skip `CREATE CATALOG` if `kaninipro_catalog` already exists (it usually does by default in a workspace).

## 3. Create volumes

Under `kaninipro_catalog.orders_etl_dev`, matching the paths in [databricks.yml](databricks.yml):

```sql
CREATE VOLUME IF NOT EXISTS kaninipro_catalog.orders_etl_dev.raw;
CREATE VOLUME IF NOT EXISTS kaninipro_catalog.orders_etl_dev.bronze;
CREATE VOLUME IF NOT EXISTS kaninipro_catalog.orders_etl_dev._checkpoints;
CREATE VOLUME IF NOT EXISTS kaninipro_catalog.orders_etl_dev.output;
```

Seed input data (required — Auto Loader has nothing to read otherwise). Both orders
and customers land as files in their own `raw/` subfolder, which Auto Loader
watches — customers is no longer read as a single fixed CSV path:

```bash
databricks fs mkdir dbfs:/Volumes/kaninipro_catalog/orders_etl_dev/raw/orders
databricks fs mkdir dbfs:/Volumes/kaninipro_catalog/orders_etl_dev/raw/customers
databricks fs cp data/orders.csv dbfs:/Volumes/kaninipro_catalog/orders_etl_dev/raw/orders/orders.csv
databricks fs cp data/customers.csv dbfs:/Volumes/kaninipro_catalog/orders_etl_dev/raw/customers/customers.csv
```

**Windows notes:**
- Always use the `dbfs:/Volumes/...` prefix, not a bare `/Volumes/...` path. On
  Windows, `databricks fs` mangles a bare leading `/` into a backslash path and
  fails with a misleading `no such directory` error before the request ever
  reaches the API.
- The `mkdir` calls above are required, not optional cleanup: a freshly created
  Volume has no subfolders, and object storage has no concept of an empty
  directory until something exists under that prefix. `databricks fs cp` (CLI
  1.11.0) checks that the destination directory already exists before writing
  and aborts with `no such directory` instead of creating it — this is a known
  CLI bug (databricks/cli issues #1408, #5834). Run `mkdir` for a subfolder once;
  after that it exists and later `cp`s into it work directly.

To update customers later (add/change a record), drop a new CSV file into
`raw/customers/` — the next job run merges/upserts it into Bronze on `customer_id`
rather than re-reading a single static file.

## 4. Run jobs

```bash
databricks bundle run orders_etl_test_job -t dev   # pytest on serverless compute, no volumes needed
databricks bundle run orders_etl_job -t dev         # real pipeline, needs steps 2-3 done first
```

Both jobs run on serverless compute — there's no cluster to create, size, or pass an
ID for.

---

# Datasets & Data Flow

Reference: every location the pipeline reads from or writes to, based on
[databricks.yml](databricks.yml) and [src/pipeline.py](src/pipeline.py).

### Orders pipeline (append-only)

| Stage | Variable | Default path | Format | Written by |
|---|---|---|---|---|
| Auto Loader source | `orders_input_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/raw/orders` | CSV (landing files) | external — files dropped in by upstream |
| Checkpoint | `orders_checkpoint_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/_checkpoints/orders` | Auto Loader schema/offset state | `ingest_orders_autoloader` |
| **Bronze (intermediate)** | `orders_bronze_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/bronze/orders` | Delta, **append-only** | `ingest_orders_autoloader` |

### Customers pipeline (merge/upsert)

| Stage | Variable | Default path | Format | Written by |
|---|---|---|---|---|
| Auto Loader source | `customers_input_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/raw/customers` | CSV (landing files) | external — files dropped in by upstream |
| Checkpoint | `customers_checkpoint_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/_checkpoints/customers` | Auto Loader schema/offset state | `ingest_customers_autoloader` |
| **Bronze (intermediate)** | `customers_bronze_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/bronze/customers` | Delta, **merged/upserted on `customer_id`** | `ingest_customers_autoloader` |

### Final outputs (target)

| Dataset | Variable | Default path | Format | Written by |
|---|---|---|---|---|
| Enriched orders | `output_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/output/enriched_orders` | Delta (job) / Parquet (manual run default) | `transform_and_write` |
| Revenue by customer | `output_path` | `/Volumes/kaninipro_catalog/orders_etl_dev/output/revenue_by_customer` | Delta (job) / Parquet (manual run default) | `transform_and_write` |

**Data flow:** `raw/orders` → (Auto Loader, append) → `bronze/orders` ─┐
`raw/customers` → (Auto Loader, merge/upsert) → `bronze/customers` ─┴→ `build_enriched_orders` + `aggregate_revenue_by_customer` → `output/enriched_orders` + `output/revenue_by_customer`

No Silver/Gold layer exists between Bronze and the final output — `transform_and_write`
reads both Bronze tables directly and writes straight to the two output datasets in
one step.
