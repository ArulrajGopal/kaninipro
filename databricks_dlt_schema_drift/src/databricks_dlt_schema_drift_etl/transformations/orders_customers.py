from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, row_number, col
from pyspark.sql.window import Window
from pyspark.sql.types import *


# source lookup table
@dp.table(comment="customer bronze table")
def customers_bronze():
    return spark.read.table("kaninipro_catalog.etl.customer_raw").withColumn( "__insert_date", current_timestamp())
            

# source driver table
@dp.table(comment="orders bronze table")
def orders_bronze():
    return spark.readStream.table("kaninipro_catalog.etl.orders_raw").withColumn( "__insert_date", current_timestamp())
                

# final joined table
@dp.table(comment="joined orders and customers data")
def joined_table():
    return spark.sql("""select 
                            o_custkey as cust_key, 
                            date_format(o_orderdate, 'yyyy-MM') as year_month,
                            case 
                                when o_orderpriority = '1-URGENT' then 1
                                when o_orderpriority = '2-HIGH' then 2
                                when o_orderpriority = '3-MEDIUM' then 3
                                when o_orderpriority = '4-NOT SPECIFIED' then 4
                                when o_orderpriority = '5-LOW' then 5
                                end as orderpriority,
                            o_orderstatus as order_status,
                            c_mktsegment as market_segment,
                            o_totalprice as total_price
                        from Live.orders_bronze A  
                        join Live.customers_bronze B 
                        on o_custkey = c_custkey
                            """)\
                 .withColumn( "__insert_date", current_timestamp())
    

