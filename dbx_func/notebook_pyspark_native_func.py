# Databricks notebook source
from pyspark.sql.functions import when, col

# COMMAND ----------

def salary_band_convert(source_df):
    result_df = source_df.withColumn(
                    "salary_band",
                    when(col("salary").isNull(), -1)
                    .when(col("salary") >= 100000, 3)
                    .when(col("salary") >= 75000, 2)
                    .otherwise(1)
                )
    return result_df

# COMMAND ----------

source_df = spark.table("kaninipro.dev.employees")

result_df = salary_band_convert(source_df)

result_df.display()

# COMMAND ----------


