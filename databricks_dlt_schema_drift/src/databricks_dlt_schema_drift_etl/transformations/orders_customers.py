from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, row_number, col
from pyspark.sql.window import Window
from pyspark.sql.types import *


# source tables
@dp.table(
    comment="customer bronze table"
)
def customers_bronze():
    df = spark.table("kaninipro_catalog.etl.customer_raw")

    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df


# source tables
@dp.table(
    comment="orders bronze table"
)
def orders_bronze():
    df = spark.readStream.table("kaninipro_catalog.etl.orders_raw")

    timestamp_added_df = df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df



@dp.table(
    comment="aggegregated orders and customers data"
)
def agg_table():
    joined_df = spark.sql("""
                        select 
                          o_custkey, 
                          date_format(o_orderdate, 'yyyy-MM') as year_month, 
                          sum(o_totalprice) as total_price
                        from LIVE.orders_bronze A  
                        join LIVE.customers_bronze B 
                        on A.o_custkey = B.c_custkey
                        group by o_custkey, date_format(o_orderdate, 'yyyy-MM')
                            """)
    
    
    timestamp_added_df = joined_df.withColumn( "__insert_date", current_timestamp())
    return timestamp_added_df
