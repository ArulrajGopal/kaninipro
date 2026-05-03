# Databricks notebook source
spark.sql('CREATE DATABASE IF NOT EXISTS kaninipro.dev')

# COMMAND ----------

from pyspark.sql import Row

data = [Row(id=1, name='Alice', age=29),
        Row(id=2, name='Bob', age=35),
        Row(id=3, name='Charlie', age=23)]

df = spark.createDataFrame(data)

df.write.mode("overwrite").format("delta").saveAsTable("kaninipro.dev.sample_table")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro.dev.sample_table 

# COMMAND ----------

spark.sql("CREATE SHARE IF NOT EXISTS data_share")
spark.sql("ALTER SHARE data_share ADD TABLE kaninipro.dev.sample_table  WITH HISTORY")
spark.sql("CREATE RECIPIENT external_client_recipient")
spark.sql("ALTER RECIPIENT external_client_recipient SET PROPERTIES ('delta_sharing.recipient.profile' = 'true')")
spark.sql("GRANT SELECT ON SHARE data_share TO RECIPIENT external_client_recipient")   

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE RECIPIENT external_client_recipient;

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

