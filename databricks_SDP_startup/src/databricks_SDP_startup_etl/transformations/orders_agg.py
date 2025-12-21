from pyspark import pipelines as dp
from pyspark.sql.functions import count, current_timestamp
from pyspark.sql.types import *

path_prefix = "abfss://raw@kaniniprodltdemo.dfs.core.windows.net/"
storage_account = "kaniniprodltdemo"

adls_key = dbutils.secrets.get(scope="myscope", key="adls_key")
spark.conf.set(f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",adls_key)


orders_schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("order_date", DateType(), False),
    StructField("updated_at", TimestampType(), True)
])

# source tables
@dp.table(
    table_properties={"quality": "bronze"},
    comment="order bronze table"
)
def orders_bronze():
    df = spark.readStream.format("csv").schema(orders_schema).option("header", "true")\
                .load(f"{path_prefix}/orders/")
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df


product_schema = StructType([
    StructField("product_id", IntegerType(), False),
    StructField("product_name", StringType(), False),
    StructField("category", StringType(), True),
    StructField("unit_price", DecimalType(10, 2), False),
    StructField("updated_at", TimestampType(), True)
])


@dp.table(
    table_properties={"quality": "bronze"},
    comment="product bronze table"
)
def products_bronze():
    df = spark.readStream.format("csv").schema(product_schema).option("header", "true")\
                .load(f"{path_prefix}/products/")
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df


customer_schema = StructType([
    StructField("customer_id", IntegerType(), False),
    StructField("name", StringType(), False),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("updated_at", TimestampType(), True)
])

@dp.table(
    table_properties={"quality": "bronze"},
    comment="customer bronze table"
)
def customers_bronze():
    df = spark.readStream.format("csv").schema(customer_schema).option("header", "true")\
                .load(f"{path_prefix}/customers/")
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df


order_items_schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("product_id", IntegerType(), False),
    StructField("qty", IntegerType(), False),
    StructField("updated_at", TimestampType(), True)
])

@dp.table(
    table_properties={"quality": "bronze"},
    comment="order items bronze table"
)
def order_items_bronze():
    df = spark.readStream.format("csv").schema(order_items_schema).option("header", "true")\
                .load(f"{path_prefix}/order_items/")
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df

