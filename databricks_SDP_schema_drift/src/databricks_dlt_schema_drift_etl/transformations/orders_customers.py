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
  keys=["c_custkey"], 
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


@dp.table(comment="final dataset with orders and customer info")
def final_dataset():
    df_o = spark.readStream.table("LIVE.raw_orders")
    df_c = spark.read.table("LIVE.customer_deduped")
    
    joined_df = df_o.join(df_c, df_o.o_custkey == df_c.c_custkey)\
                  .selectExpr("c_custkey as cust_key",
                              "o_orderdate as order_date",
                              "o_orderkey as order_key",
                              "o_orderstatus as order_status",
                              "o_totalprice as total_price",
                              "o_orderpriority as order_priority"
                              )\
                  .withColumn( "__created_time", current_timestamp())        
    return joined_df
