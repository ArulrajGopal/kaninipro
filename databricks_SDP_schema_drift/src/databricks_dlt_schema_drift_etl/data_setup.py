# Databricks notebook source
# MAGIC %md
# MAGIC #catalog, schema and table setup

# COMMAND ----------

spark.sql("CREATE CATALOG if not exists kaninipro_catalog")

# COMMAND ----------

spark.sql("CREATE database if not exists kaninipro_catalog.etl")

# COMMAND ----------

spark.sql("""
CREATE TABLE kaninipro_catalog.etl.customer_raw
AS
SELECT * FROM samples.tpch.customer
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC select min(o_orderdate) as min_date, max(o_orderdate) as max_orderdate from samples.tpch.orders

# COMMAND ----------


orders = spark.sql("select * from samples.tpch.orders where o_orderdate <= '1996-04-30'")
orders.write.mode("append").saveAsTable("kaninipro_catalog.etl.orders_raw")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.joined_table;

# COMMAND ----------

# MAGIC %md
# MAGIC #sample code

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

df_joined = spark.sql("""
    select 
        o_custkey as cust_key, 
        date_format(o_orderdate, 'yyyy-MM') as year_month,
        o_orderstatus as order_status,
        c_mktsegment as market_segment,
        o_totalprice as total_price
    from kaninipro_catalog.dev.orders_bronze A  
    join kaninipro_catalog.dev.customers_bronze B 
    on o_custkey = c_custkey
""").withColumn("__insert_date", current_timestamp())

# COMMAND ----------

spark.sql("""
ALTER TABLE kaninipro_catalog.dev.joined_table
ADD COLUMNS (
    order_status STRING,
    market_segment STRING
)
""")

# COMMAND ----------

# Backfill historical data for joined_table after schema change using SQL UPDATE (only order_status & market_segment)
spark.sql("""
MERGE INTO kaninipro_catalog.dev.joined_table AS target
USING (
    SELECT
        o.o_custkey AS cust_key,
        o.o_orderdate,
        o.o_orderstatus AS order_status,
        c.c_mktsegment AS market_segment
    FROM kaninipro_catalog.dev.orders_bronze o
    JOIN kaninipro_catalog.dev.customers_bronze c
      ON o.o_custkey = c.c_custkey
) AS source
ON target.cust_key = source.cust_key 
AND target.year_month = date_format(source.o_orderdate, 'yyyy-MM')
WHEN MATCHED THEN UPDATE SET
    target.order_status = source.order_status,
    target.market_segment = source.market_segment
""")



