"""Orders ETL pipeline entry point.

Runs as a Databricks Job via the `notebook_task` in
resources/orders_etl_job.yml, which calls into this module from
src/orders_etl_notebook.py. `get_spark_session()` uses `getOrCreate()`, so on
a Databricks cluster it simply attaches to the runtime's existing session.

Both orders and customers are ingested via Databricks Auto Loader: incremental
ingestion of new files from an ADLS location (a Unity Catalog Volume) into a
Bronze Delta table, then a batch read of that table. There is no alternative
(e.g. plain CSV) loading path for either. Orders land append-only (each row
is an immutable event); customers are merged/upserted on `customer_id`
(SCD-Type-1), since a customer record can be updated in place.
"""

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession

from src.schemas import CUSTOMERS_SCHEMA, ORDERS_SCHEMA
from src.transformations import (
    add_order_total,
    aggregate_revenue_by_customer,
    categorize_orders,
    clean_orders,
    deduplicate_orders,
    join_customer_region,
)


def get_spark_session(app_name: str = "orders-etl-pipeline") -> SparkSession:
    return SparkSession.builder.appName(app_name).getOrCreate()


def ingest_orders_autoloader(
    spark: SparkSession,
    input_path: str,
    bronze_path: str,
    checkpoint_path: str,
) -> None:
    """Land any new order CSV files from `input_path` into a Bronze Delta table.

    Uses Databricks Auto Loader (`cloudFiles`) with `trigger(availableNow=True)`,
    so each pipeline run picks up whatever files have arrived since the last run
    and then exits, instead of running as a continuous streaming job. The
    dedup/aggregation transformations need full-dataset batch semantics (window
    functions, groupBy) that structured streaming doesn't support, so the
    Bronze table is read back as an ordinary batch DataFrame afterwards.
    """
    stream_df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", f"{checkpoint_path}/schema")
        .option("header", "true")
        .schema(ORDERS_SCHEMA)
        .load(input_path)
    )
    query = (
        stream_df.writeStream.format("delta")
        .option("checkpointLocation", checkpoint_path)
        .outputMode("append")
        .trigger(availableNow=True)
        .start(bronze_path)
    )
    query.awaitTermination()


def read_orders_bronze(spark: SparkSession, bronze_path: str) -> DataFrame:
    """Batch-read the Bronze Delta table populated by `ingest_orders_autoloader`."""
    return spark.read.format("delta").load(bronze_path)


def ingest_customers_autoloader(
    spark: SparkSession,
    input_path: str,
    bronze_path: str,
    checkpoint_path: str,
) -> None:
    """Land any new/changed customer CSV files from `input_path` into a Bronze
    Delta table, merging (upserting) on `customer_id` instead of appending.

    Unlike orders, a customer record can be updated (name/region changes), so
    each Auto Loader micro-batch is merged into Bronze (SCD-Type-1: matching
    rows are overwritten in place, new customer_ids are inserted) rather than
    just appended. The target table doesn't exist on the very first run, so
    that batch instead does a plain write to create it.
    """

    def upsert_batch(batch_df: DataFrame, batch_id: int) -> None:
        # MERGE requires at most one matching source row per target row.
        batch_df = batch_df.dropDuplicates(["customer_id"])
        if DeltaTable.isDeltaTable(spark, bronze_path):
            (
                DeltaTable.forPath(spark, bronze_path)
                .alias("target")
                .merge(batch_df.alias("source"), "target.customer_id = source.customer_id")
                .whenMatchedUpdateAll()
                .whenNotMatchedInsertAll()
                .execute()
            )
        else:
            batch_df.write.format("delta").mode("overwrite").save(bronze_path)

    stream_df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", f"{checkpoint_path}/schema")
        .option("header", "true")
        .schema(CUSTOMERS_SCHEMA)
        .load(input_path)
    )
    query = (
        stream_df.writeStream.foreachBatch(upsert_batch)
        .option("checkpointLocation", checkpoint_path)
        .trigger(availableNow=True)
        .start()
    )
    query.awaitTermination()


def read_customers_bronze(spark: SparkSession, bronze_path: str) -> DataFrame:
    """Batch-read the Bronze Delta table populated by `ingest_customers_autoloader`."""
    return spark.read.format("delta").load(bronze_path)


def build_enriched_orders(orders_df: DataFrame, customers_df: DataFrame) -> DataFrame:
    """Apply the full cleaning/enrichment chain to raw orders + customers."""
    orders_df = clean_orders(orders_df)
    orders_df = deduplicate_orders(orders_df)
    orders_df = add_order_total(orders_df)
    orders_df = categorize_orders(orders_df)
    return join_customer_region(orders_df, customers_df)


def transform_and_write(
    orders_df: DataFrame,
    customers_df: DataFrame,
    output_path: str,
    write_format: str = "parquet",
) -> None:
    """Enrich, aggregate, and write orders/customers DataFrames.

    Takes already-loaded DataFrames rather than paths, so it has no
    dependency on how orders were ingested (Auto Loader vs. anything else) -
    this is what makes it testable with in-memory DataFrames.
    """
    enriched_orders = build_enriched_orders(orders_df, customers_df)
    revenue_by_customer = aggregate_revenue_by_customer(enriched_orders)

    enriched_orders.write.mode("overwrite").format(write_format).save(f"{output_path}/enriched_orders")
    revenue_by_customer.write.mode("overwrite").format(write_format).save(f"{output_path}/revenue_by_customer")


def run_pipeline(
    spark: SparkSession,
    output_path: str,
    orders_input_path: str,
    orders_bronze_path: str,
    orders_checkpoint_path: str,
    customers_input_path: str,
    customers_bronze_path: str,
    customers_checkpoint_path: str,
    write_format: str = "parquet",
) -> None:
    """Run the pipeline end to end.

    Ingests new order files from `orders_input_path` into `orders_bronze_path`
    via Auto Loader (append-only), and new/changed customer files from
    `customers_input_path` into `customers_bronze_path` via Auto Loader
    (merged/upserted on `customer_id`), each checkpointed at their own
    `*_checkpoint_path`. Both Bronze tables are then read back as batch
    DataFrames. This is the only supported loading path for either.
    """
    ingest_orders_autoloader(spark, orders_input_path, orders_bronze_path, orders_checkpoint_path)
    orders_df = read_orders_bronze(spark, orders_bronze_path)

    ingest_customers_autoloader(spark, customers_input_path, customers_bronze_path, customers_checkpoint_path)
    customers_df = read_customers_bronze(spark, customers_bronze_path)

    transform_and_write(orders_df, customers_df, output_path, write_format)

