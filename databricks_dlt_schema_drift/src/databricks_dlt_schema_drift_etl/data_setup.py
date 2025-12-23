# Databricks notebook source

# COMMAND ----------

spark.sql("CREATE CATALOG if not exists kaninipro_catalog")
spark.sql("CREATE database if not exists kaninipro_catalog.etl")


# COMMAND ----------

spark.sql("""
CREATE TABLE kaninipro_catalog.etl.customer_raw
AS
SELECT * FROM samples.tpch.customer
""")

# COMMAND ----------
display(spark.sql("select min(o_orderdate) as min_date, max(o_orderdate) as max_orderdate from samples.tpch.orders"))


# COMMAND ----------
orders = spark.sql("select * from samples.tpch.orders where o_orderdate <= '1995-12-31'")
orders.write.saveAsTable("kaninipro_catalog.etl.orders_raw")

# COMMAND ----------
spark.sql("""
select o_custkey, date_format(o_orderdate, 'yyyy-MM') as year_month, sum(o_totalprice) from kaninipro_catalog.etl.orders_raw A  
join kaninipro_catalog.etl.customer_raw B 
on A.o_custkey = B.c_custkey
group by o_custkey, date_format(o_orderdate, 'yyyy-MM')
""")

