# Databricks notebook source
from pyspark.sql.functions import col,current_timestamp,lit
spark.sql("CREATE SCHEMA IF NOT EXISTS kaninipro_catalog.dev")
spark.sql("CREATE VOLUME IF NOT EXISTS kaninipro_catalog.dev.landing_zone")

# COMMAND ----------

# MAGIC %md
# MAGIC #initial load setup

# COMMAND ----------

df = spark.table("samples.tpch.customer")\
        .filter(col("c_custkey")<=100000)\
        .withColumn("__insert_time",current_timestamp())\
        .coalesce(10)

df.write.mode("overwrite").format("parquet").save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------

# MAGIC %md
# MAGIC #batch1 setup

# COMMAND ----------

from pyspark.sql.types import DecimalType

df = spark.table("samples.tpch.customer")

batch1_df = df.filter(col("c_custkey")<=4)\
                    .withColumn("c_acctbal",lit(0.00).cast(DecimalType(18,2)))\
                    .withColumn("__insert_time",lit("2025-12-26T18:59:48.469+00:00"))

batch2_df = df.withColumn("c_acctbal",lit(15.00).cast(DecimalType(18,2)))\
                    .filter(col("c_custkey")<=2)\
                    .withColumn("__insert_time",current_timestamp())

incr_df = batch1_df.unionByName(batch2_df).coalesce(1)

incr_df.write.mode("append").format("parquet").save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------



# COMMAND ----------

