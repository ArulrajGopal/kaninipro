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

dbutils.fs.rm("/Volumes/kaninipro_catalog/dev/landing_zone/customers",True)

# COMMAND ----------

df = spark.table("samples.tpch.customer")\
        .filter(col("c_custkey")<=100000)\
        .withColumn("__insert_time",current_timestamp())\
        .coalesce(1)

df.write.mode("overwrite").format("parquet")\
                .save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------

# MAGIC %md
# MAGIC #Incr load setup

# COMMAND ----------

from pyspark.sql.types import DecimalType

df = spark.table("samples.tpch.customer")

df_1 = df.filter(col("c_custkey")<=4)\
                    .withColumn("c_acctbal",lit(0.00).cast(DecimalType(18,2)))\
                    .withColumn("__insert_time",lit("2025-12-27T07:50:00.000+00:00"))

df_2 = df.withColumn("c_acctbal",lit(15.00).cast(DecimalType(18,2)))\
                    .filter(col("c_custkey")<=2)\
                    .withColumn("__insert_time",current_timestamp())

incr_df = df_1.unionByName(df_2).coalesce(1)

incr_df.write.mode("append").format("parquet").save("/Volumes/kaninipro_catalog/dev/landing_zone/customers")

# COMMAND ----------

display(incr_df)

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

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.customers_deduped where c_custkey <= 4

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro_catalog.dev.customers_history  
# MAGIC where c_custkey <= 4
# MAGIC order by c_custkey, __START_AT 

# COMMAND ----------



# COMMAND ----------

