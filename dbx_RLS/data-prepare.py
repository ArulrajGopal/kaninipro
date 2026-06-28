# Databricks notebook source
from pyspark.sql.functions import col

# COMMAND ----------

df = spark.table("samples.bakehouse.sales_customers")\
        .filter(col("continent").isin("North America","Asia"))
df.write.mode("overwrite").format("delta").saveAsTable("kaninipro.dev.sales_customers")

# COMMAND ----------

# MAGIC %sql
# MAGIC select current_user();

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro.dev.sales_customers

# COMMAND ----------

