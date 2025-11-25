# Databricks notebook source
import json

env = dbutils.widgets.get("env")

config_path = "../config/my_project.json"
with open(config_path, "r") as f:
    config = json.load(f).get(env, {})


# COMMAND ----------

storage_account = config["storage_account"]
input_path = config["employee_department_path"]
output_path = config["employee_department_target"]

# COMMAND ----------

adls_key = dbutils.secrets.get(scope="myscope", key="adls_key")
spark.conf.set(f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",adls_key)

# COMMAND ----------

from pyspark.sql.types import *

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("employee_name", StringType(), True),
    StructField("department", StringType(), True)
])

df = spark.read.format("csv")\
            .option("Header",True)\
            .schema(schema) \
            .load(input_path)

dbutils.fs.rm(output_path, True)

df.write.mode("overwrite").format("parquet").save(output_path)