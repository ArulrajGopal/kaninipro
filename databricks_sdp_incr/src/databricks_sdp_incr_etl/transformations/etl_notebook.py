from pyspark import pipelines as dp
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

catalog = "kaninipro_catalog"
database = "dev"
catalog_database = f"{catalog}.{database}"
path = "/Volumes/kaninipro_catalog/dev/landing_zone/customers/"


# Create the target bronze table
dp.create_streaming_table("raw_customers", comment="New customer data incrementally ingested from cloud object storage landing zone")

# Create an Append Flow to ingest the raw data into the bronze table
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