# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW STORAGE CREDENTIALS

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS kanini_prometastore_dev
# MAGIC   URL 'abfss://data@kaniniprometastoredev.dfs.core.windows.net/'
# MAGIC   WITH (STORAGE CREDENTIAL kaninipro_cred);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG kaninipro_catalog
# MAGIC MANAGED LOCATION 'abfss://data@kaniniprometastoredev.dfs.core.windows.net/';

# COMMAND ----------

# MAGIC %sql
# MAGIC show catalogs;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS kaninipro.dev;

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog kaninipro;
# MAGIC show databases;