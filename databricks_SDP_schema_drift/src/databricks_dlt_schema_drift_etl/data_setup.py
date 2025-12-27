# Databricks notebook source
from pyspark.sql.functions import col

# COMMAND ----------

# MAGIC %md
# MAGIC #catalog, schema and table setup

# COMMAND ----------

spark.sql("CREATE CATALOG if not exists kaninipro_catalog")
spark.sql("CREATE database if not exists kaninipro_catalog.dev")

# COMMAND ----------

# customer data
spark.table("samples.tpch.customer")\
    .write.mode("append")\
    .format("parquet")\
    .save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------

# MAGIC %sql
# MAGIC select min(o_orderdate) as min_date, max(o_orderdate) as max_orderdate from samples.tpch.orders

# COMMAND ----------

# orders data batch1
spark.table("samples.tpch.orders")\
    .filter(col("o_orderdate").between("1992-01-01","1992-12-31"))\
    .write.mode("append")\
    .format("parquet")\
    .save("/Volumes/kaninipro_catalog/dev/landing_zone/orders")

# COMMAND ----------

# orders data batch2
spark.table("samples.tpch.orders")\
    .filter(col("o_orderdate").between("1993-01-01","1993-03-31"))\
    .write.mode("append")\
    .format("parquet")\
    .save("/Volumes/kaninipro_catalog/dev/landing_zone/orders")

# COMMAND ----------

# orders data batch3
spark.table("samples.tpch.orders")\
    .filter(col("o_orderdate").between("1993-04-01","1993-06-30"))\
    .write.mode("append")\
    .format("parquet")\
    .save("/Volumes/kaninipro_catalog/dev/landing_zone/orders")

# COMMAND ----------

# MAGIC %md
# MAGIC #Explore

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.final_dataset

# COMMAND ----------

# MAGIC %md
# MAGIC #Queries to fix data manually

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE kaninipro_catalog.dev.final_dataset
# MAGIC ALTER COLUMN order_priority TYPE INT;
# MAGIC
# MAGIC ALTER TABLE kaninipro_catalog.dev.final_dataset
# MAGIC ADD COLUMNS (market_segment STRING);
# MAGIC   

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     c.c_custkey        AS cust_key,
# MAGIC     o.o_orderdate      AS order_date,
# MAGIC     o.o_orderkey       AS order_key,
# MAGIC     o.o_orderstatus    AS order_status,
# MAGIC     o.o_totalprice     AS total_price,
# MAGIC     CASE
# MAGIC         WHEN o.o_orderpriority = '1-URGENT'        THEN 1
# MAGIC         WHEN o.o_orderpriority = '2-HIGH'          THEN 2
# MAGIC         WHEN o.o_orderpriority = '3-MEDIUM'        THEN 3
# MAGIC         WHEN o.o_orderpriority = '4-NOT SPECIFIED' THEN 4
# MAGIC         WHEN o.o_orderpriority = '5-LOW'           THEN 5
# MAGIC     END                  AS order_priority,
# MAGIC     c.c_mktsegment      AS market_segment,
# MAGIC     current_timestamp() AS __created_time
# MAGIC FROM LIVE.raw_orders o
# MAGIC JOIN LIVE.customer_deduped c
# MAGIC   ON o.o_custkey = c.c_custkey;
# MAGIC

# COMMAND ----------

spark.sql("""
MERGE INTO kaninipro_catalog.dev.target_table AS t
USING (
  SELECT
    c.c_custkey        AS cust_key,
    o.o_orderdate      AS order_date,
    o.o_orderkey       AS order_key,
    o.o_orderstatus    AS order_status,
    o.o_totalprice     AS total_price,
    CASE
        WHEN o.o_orderpriority = '1-URGENT' THEN 1
        WHEN o.o_orderpriority = '2-HIGH' THEN 2
        WHEN o.o_orderpriority = '3-MEDIUM' THEN 3
        WHEN o.o_orderpriority = '4-NOT SPECIFIED' THEN 4
        WHEN o.o_orderpriority = '5-LOW' THEN 5
        ELSE NULL
    END AS order_priority,
    c.c_mktsegment      AS market_segment,
    current_timestamp() AS __created_time
  FROM LIVE.raw_orders o
  JOIN LIVE.customer_deduped c
    ON o.o_custkey = c.c_custkey
) AS s
ON t.cust_key = s.cust_key AND t.order_key = s.order_key
WHEN MATCHED THEN
  UPDATE SET
    t.order_priority = s.order_priority,
    t.market_segment = s.market_segment
""")