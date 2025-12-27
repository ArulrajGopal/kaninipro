# Databricks notebook source
spark.sql("CREATE CATALOG IF NOT EXISTS kaninipro_catalog")
spark.sql("CREATE SCHEMA IF NOT EXISTS kaninipro_catalog.dev")
spark.sql("CREATE VOLUME IF NOT EXISTS kaninipro_catalog.dev.landing_zone")

# COMMAND ----------

from pyspark.sql.functions import col,current_timestamp,lit

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
# MAGIC #Incr load setup

# COMMAND ----------

from pyspark.sql.types import DecimalType

df = spark.table("samples.tpch.customer")

batch1_df = df.filter(col("c_custkey")<=4)\
                    .withColumn("c_acctbal",lit(0.00).cast(DecimalType(18,2)))\
                    .withColumn("__insert_time",lit("2025-12-27T06:25:32.710+00:00"))

batch2_df = df.withColumn("c_acctbal",lit(15.00).cast(DecimalType(18,2)))\
                    .filter(col("c_custkey")<=2)\
                    .withColumn("__insert_time",current_timestamp())

incr_df = batch1_df.unionByName(batch2_df).coalesce(1)

incr_df.write.mode("append").format("parquet").save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------

# MAGIC %md
# MAGIC #exploring

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.customers_deduped

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.customers_deduped where c_custkey <= 4

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

