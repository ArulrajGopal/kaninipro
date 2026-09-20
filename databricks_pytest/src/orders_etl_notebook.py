# Databricks notebook source
# MAGIC %md
# MAGIC # Orders ETL
# MAGIC Notebook entry point for the Orders ETL Databricks Job (see
# MAGIC `resources/orders_etl_job.yml`). Reads orders/customers data, cleans and
# MAGIC enriches it, aggregates revenue by customer, and writes both outputs.
# MAGIC
# MAGIC The actual transformation logic lives in `src/pipeline.py` /
# MAGIC `src/transformations.py` and is imported here rather than duplicated.
# MAGIC
# MAGIC Orders and customers are both always sourced via Auto Loader from ADLS
# MAGIC locations backing Unity Catalog Volumes, landing incrementally into
# MAGIC their own Bronze Delta tables before the batch transformations run.
# MAGIC Orders land append-only; customers are merged/upserted on customer_id.

# COMMAND ----------

import os
import sys

# The bundle syncs the whole repo, so the notebook's parent directory is the
# repo root — add it to the path to import the `src` package.
sys.path.append(os.path.abspath(".."))

from src.pipeline import get_spark_session, run_pipeline

# COMMAND ----------

dbutils.widgets.text("orders_input_path", "")
dbutils.widgets.text("orders_bronze_path", "")
dbutils.widgets.text("orders_checkpoint_path", "")
dbutils.widgets.text("customers_input_path", "")
dbutils.widgets.text("customers_bronze_path", "")
dbutils.widgets.text("customers_checkpoint_path", "")
dbutils.widgets.text("output_path", "/Volumes/kaninipro_catalog/orders_etl_dev/output")
dbutils.widgets.text("format", "parquet")

orders_input_path = dbutils.widgets.get("orders_input_path")
orders_bronze_path = dbutils.widgets.get("orders_bronze_path")
orders_checkpoint_path = dbutils.widgets.get("orders_checkpoint_path")
customers_input_path = dbutils.widgets.get("customers_input_path")
customers_bronze_path = dbutils.widgets.get("customers_bronze_path")
customers_checkpoint_path = dbutils.widgets.get("customers_checkpoint_path")
output_path = dbutils.widgets.get("output_path")
write_format = dbutils.widgets.get("format")

# COMMAND ----------

spark_session = get_spark_session()
run_pipeline(
    spark=spark_session,
    output_path=output_path,
    write_format=write_format,
    orders_input_path=orders_input_path,
    orders_bronze_path=orders_bronze_path,
    orders_checkpoint_path=orders_checkpoint_path,
    customers_input_path=customers_input_path,
    customers_bronze_path=customers_bronze_path,
    customers_checkpoint_path=customers_checkpoint_path,
)
