# Databricks notebook source
import pandas as pd
from pyspark.sql.functions import pandas_udf, col
from pyspark.sql.types import IntegerType


@pandas_udf(IntegerType())
def salary_band(salary: pd.Series) -> pd.Series:
    return salary.map(
        lambda s: -1 if s is None else
        3 if s >= 100000 else
        2 if s >= 75000 else 1
    )


# COMMAND ----------

df = spark.table("kaninipro.dev.employees")

result_df = df.withColumn("salary_band",  salary_band(col("salary"))) 

result_df.display()

