from pyspark import pipelines as dp
from pyspark.sql.functions import col

catalog = "kaninipro_catalog"
database = "dev"
catalog_database = f"{catalog}.{database}"
path = "/Volumes/kaninipro_catalog/dev/landing/"



order_rules = {
  "order priority rule" : "o_orderpriority in ('1-URGENT','2-HIGH')",
  "order total price": "o_totalprice > 100000"
}


@dp.expect_all_or_fail(order_rules)
@dp.table(comment="orders cleaned")
def order_validated():
    df = spark.table(f"{catalog_database}.raw_orders")
    return df

  