# Databricks notebook source
dbutils.widgets.text("catalog", "kaninipro")
dbutils.widgets.text("schema", "dev")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

source_table = f"{catalog}.{schema}.Employees"
target_table = f"{catalog}.{schema}.employees_daily_summary"

# COMMAND ----------

from pyspark.sql import functions as F

employees_df = spark.table(source_table)

summary_df = (
    employees_df
    .withColumn("last_modified_date", F.to_date("LastModifiedTime"))
    .groupBy("last_modified_date")
    .agg(F.count("EmployeeID").alias("employee_count"))
    .orderBy("last_modified_date")
)

summary_df.write.mode("overwrite").saveAsTable(target_table)

display(summary_df)
