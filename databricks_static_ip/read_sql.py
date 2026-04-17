# Databricks notebook source
my_password = "<your_password_here>"
user_id = "<your_user_id_here>"

# COMMAND ----------

jdbcHostname = "kaninipro-server.database.windows.net"
jdbcPort = 1433
database = "kaninipro_db"

jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};database={database};encrypt=false;trustServerCertificate=true"

connectionProperties = {
  "user": user_id,
  "password": my_password,
  "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

df = spark.read.jdbc(
    url=jdbcUrl,
    table="Students",
    properties=connectionProperties
)

display(df)

# 