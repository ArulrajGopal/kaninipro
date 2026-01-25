from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, col,to_date
from pyspark.sql.types import *

storage_account = "kaniniprodltdemo"
raw_path_prefix = f"abfss://raw@{storage_account}.dfs.core.windows.net/"
target_path_prefix = f"abfss://target@{storage_account}.dfs.core.windows.net/"


adls_key = dbutils.secrets.get(scope="myscope", key="adls_key")
spark.conf.set(f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",adls_key)


orders_schema = StructType([
    StructField("order_id", IntegerType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("order_date", StringType(), False),
    StructField("product_id", IntegerType(), False),
    StructField("qty", IntegerType(), False)
])


@dp.table(
    table_properties={"quality": "bronze"},
    comment="order bronze table"
)
def orders_bronze():
    df = spark.readStream.format("csv").schema(orders_schema).option("header", "true")\
                .load(f"{raw_path_prefix}/orders/")\
                .withColumn("order_date",to_date(col("order_date"), "dd-MM-yyyy")
)
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df




product_schema = StructType([
    StructField("product_id", IntegerType(), False),
    StructField("product_name", StringType(), False),
    StructField("category", StringType(), True),
    StructField("unit_price", DecimalType(10, 2), False)
])

@dp.table(
    table_properties={"quality": "bronze"},
    comment="product bronze table"
)
def products_bronze():
    df = spark.readStream.format("csv").schema(product_schema).option("header", "true")\
                .load(f"{raw_path_prefix}/products/")
    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df


dp.create_sink(
    name="parquet_sink",
    format="parquet",
    options={"path": f"{target_path_prefix}/final_data/"}
)

@dp.append_flow(
    target="parquet_sink"
)
def final_data_sink():
    orders = spark.readStream.table("LIVE.orders_bronze")
    products = spark.readStream.table("LIVE.products_bronze")
    
    joined_df = orders.alias("A").join(products.alias("B"),["product_id"])\
                        .selectExpr("A.order_id",
                                    "A.customer_id",
                                    "A.order_date",
                                    "A.product_id",
                                    "A.qty",
                                    "B.product_name",
                                    "B.category",
                                    "B.unit_price")\
                        .withColumn( "__processed_time", current_timestamp())
    return joined_df



@dp.table(
    comment = "aggregated_table"
)
def agg_data():
    orders = spark.table("LIVE.orders_bronze")
    products = spark.table("LIVE.products_bronze")
    
    joined_df = orders.alias("A").join(
                    products.alias("B"),
                    ["product_id"]
                        ).selectExpr(
                            "A.customer_id",
                            "A.qty * B.unit_price as total_value",
                            "date_format(A.order_date, 'yyyy-MM') as year_month"
                        )\
                    .withColumn( "__processed_time", current_timestamp())
       
    return joined_df

