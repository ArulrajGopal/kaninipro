from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, col


catalog = "kaninipro_catalog"
database = "dev"
catalog_database = f"{catalog}.{database}"
volumn_path = "/Volumes/kaninipro_catalog/dev/landing_zone/"

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
          .load(f"{volumn_path}/customers")
          .withColumn( "__created_time", current_timestamp())
  )

dp.create_streaming_table(name="customer_deduped", comment="customer deduped table")

dp.create_auto_cdc_flow(
  target="customer_deduped",  
  source="raw_customers",  
  keys=["cust_key"], 
  sequence_by=col("__created_time")
)


dp.create_streaming_table("raw_orders", comment="Incremental load")

@dp.append_flow(
  target = "raw_orders"
)
def raw_orders():
  return (
      spark.readStream
          .format("cloudFiles")
          .option("cloudFiles.format", "parquet")
          .option("cloudFiles.inferColumnTypes", "true")
          .load(f"{volumn_path}/orders")
          .withColumn( "__created_time", current_timestamp())
  )



@dp.table(comment="customer bronze table")
def joined_table():
    df_o = spark.readStream.table("LIVE.raw_orders")
    df_c = spark.read.table("LIVE.customer_deduped")
    
    joined_df = df_o.join(df_c, df_o.o_custkey == df_c.c_custkey)\
                  .selectExpr("c_custkey as cust_key",
                              "o_orderdate as order_date",
                              "o_orderkey as order_key",
                              "o_orderpriority as order_priority",
                              "o_orderstatus as order_status",
                              "o_totalprice as total_price"
                              )\
                  .withColumn( "__created_time", current_timestamp())        
    return joined_df



dp.create_streaming_table(name="final_dataset", comment="fully joined table")

dp.create_auto_cdc_flow(
  target="final_dataset",  
  source="joined_table",  
  keys=["cust_key","order_key"], 
  sequence_by=col("__created_time"),
  stored_as_scd_type="2"
)
