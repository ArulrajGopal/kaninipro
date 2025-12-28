# Databricks notebook source

# COMMAND ----------
spark.sql("CREATE DATABASE IF NOT EXISTS kaninipro_catalog.dev")
spark.sql("CREATE VOLUME IF NOT EXISTS kaninipro_catalog.dev.LANDING")

# COMMAND ----------
from pyspark.sql.functions import col, current_timestamp

# COMMAND ----------
spark.table("samples.tpch.orders")\
        .filter(col("o_orderkey")<=100)\
        .withColumn("__loaded_time", current_timestamp())\
        .coalesce(1)\
        .write.mode("overwrite").format("parquet")\
        .save("/Volumes/kaninipro_catalog/dev/landing/orders")