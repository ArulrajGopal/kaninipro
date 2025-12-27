from pyspark import pipelines as dp
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

catalog = "kaninipro_catalog"
database = "dev"
catalog_database = f"{catalog}.{database}"
path = "/Volumes/kaninipro_catalog/dev/landing_zone/customers/"

dp.create_streaming_table("raw_customers", comment="Incremental load")

@dp.append_flow(
  target = "raw_customers"
)
def raw_customers():
  return (
      spark.readStream
          .format("cloudFiles")
          .option("cloudFiles.format", "parquet")
          .option("cloudFiles.inferColumnTypes", "true")
          .load(f"{path}")
  )


dp.create_streaming_table(name="customers_deduped", comment="Deduped")

dp.create_auto_cdc_flow(
  target="customers_deduped",  
  source="raw_customers",  
  keys=["c_custkey"], 
  sequence_by=col("__insert_time")
)


dp.create_streaming_table(
    name="customers_history", comment="SCD type 2 for customers"
)

dp.create_auto_cdc_flow(
    target="customers_history",
    source="raw_customers",
    keys=["c_custkey"],
    sequence_by=col("__insert_time"),
    stored_as_scd_type="2",
)  


