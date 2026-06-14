# Databricks notebook source
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, DoubleType, IntegerType


@udf(returnType=IntegerType())
def salary_band(salary):
    if salary is None: return -1
    if salary >= 100000: return 3
    elif salary >= 75000: return 2
    else: return 1


# COMMAND ----------

df = spark.table("kaninipro.dev.employees")

result_df = df.withColumn("salary_band",     salary_band(col("salary")))

result_df.display()

# COMMAND ----------

spark.udf.register("salary_band",     salary_band)
df = spark.table("kaninipro.dev.employees")

result_df1 = df.selectExpr(
    "id",
    "salary_band(salary)      AS salary_band"
)
result_df1.display()


