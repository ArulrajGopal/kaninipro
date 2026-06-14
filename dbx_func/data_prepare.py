# Databricks notebook source
spark.sql("create database if not exists kaninipro.dev")

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

data = [
    (1, "Alice", 30, "Engineering", 95000.0),
    (2, "Bob",   25, "Marketing",   72000.0),
    (3, "Carol", 35, "Engineering", 110000.0),
    (4, "David", 28, "HR",          65000.0),
    (5, "Eve",   32, "Marketing",   80000.0),
]

schema = StructType([
    StructField("id",         IntegerType(), False),
    StructField("name",       StringType(),  True),
    StructField("age",        IntegerType(),  True),
    StructField("department", StringType(),  True),
    StructField("salary",     DoubleType(),  True),
])

df = spark.createDataFrame(data, schema=schema)
df.write.mode("overwrite").format("delta").saveAsTable("kaninipro.dev.employees")