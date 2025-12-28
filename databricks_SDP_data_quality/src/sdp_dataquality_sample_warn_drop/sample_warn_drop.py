from pyspark import pipelines as dp
from pyspark.sql.functions import col

catalog = "kaninipro_catalog"
database = "dev"
catalog_database = f"{catalog}.{database}"
path = "/Volumes/kaninipro_catalog/dev/landing/"

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
          .load(f"{path}/orders")
  )


order_rules = {
  "order priority rule" : "o_orderpriority in ('1-URGENT','2-HIGH')",
  "order total price": "o_totalprice > 100000"
}


@dp.expect_all(order_rules)
@dp.table(comment="orders full")
def order_full():
    df = spark.table("LIVE.raw_orders")
    return df
  
@dp.expect_all_or_drop(order_rules)
@dp.table(comment="orders cleaned")
def order_cleaned():
    df = spark.table("LIVE.raw_orders")
    return df
  

  