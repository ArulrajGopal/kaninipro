from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, row_number, col
from pyspark.sql.window import Window
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
                .load(f"{path_prefix}/product/")
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
                .load(f"{path_prefix}/customer/")
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



@dp.table(
    table_properties={"quality": "silver"},
    comment="joined_table"
)
def joined_silver():
    joined_df = spark.sql("""
                            select 
                                A.*,
                                B.order_id, 
                                B.qty,
                                (B.qty * A.unit_price) as total_order_value,
                                C.customer_id,
                                C.order_date,
                                D.name as customer_name
                            from kaninipro_catalog.demo.products_bronze A  
                            join kaninipro_catalog.demo.order_items_bronze B 
                            on A.product_id = B.product_id 
                            join kaninipro_catalog.demo.orders_bronze C 
                            on C.order_id = B.order_id 
                            join kaninipro_catalog.demo.customers_bronze D 
                            on C.customer_id = D.customer_id
                            """)
    
    
    timestamp_added_df = joined_df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df



@dp.table(
    table_properties={"quality": "gold"},
    comment="orders_agg"
)
def orders_agg():

    order_value_agg = spark.sql("""
    select 
    customer_name,
    customer_id,
    TO_CHAR(order_date, 'yyyy-MM') as year_month,
    sum(total_order_value) as total_order_value_sum
    from kaninipro_catalog.demo.joined_silver
    group by year_month, customer_name, customer_id
    """)

    window_spec = Window.partitionBy("year_month").orderBy(order_value_agg["total_order_value_sum"].desc())
    order_value_agg = order_value_agg.withColumn("rank", row_number().over(window_spec)).filter(col("rank") == 1).drop("rank")

    filtered_df = order_value_agg.filter(col("rank") == 1).drop("rank")

    timestamp_added_df = filtered_df.withColumn( "__insert_date", current_timestamp())

    return timestamp_added_df
