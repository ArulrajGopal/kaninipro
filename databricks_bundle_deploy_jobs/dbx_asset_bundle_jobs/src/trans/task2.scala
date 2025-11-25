// Databricks notebook source
val env = dbutils.widgets.get("env")

val dfCollected = spark.read.option("multiline", "true")
            .format("json").load(s"file:/Workspace/Users/arulrajgopal@outlook.com/.bundle/my_project/$env/files/src/config/my_project.json")
            .select(s"$env").collect()

val row = dfCollected(0).getStruct(0)
val storage_account = row.getAs[String]("storage_account")
val input_path = row.getAs[String]("employee_salary_path")
val output_path = row.getAs[String]("employee_salary_target")

// COMMAND ----------

val adls_key = dbutils.secrets.get(scope="myscope", key="adls_key")
spark.conf.set(s"fs.azure.account.key.$storage_account.dfs.core.windows.net",adls_key)

// COMMAND ----------

import org.apache.spark.sql.types._

val schema = StructType(
  Array(
    StructField("id", IntegerType, true),
    StructField("salary", LongType, true),
    StructField("designation", StringType, true)
  )
)

val df = spark.read.format("csv")
            .option("Header",true)
            .schema(schema) 
            .load(input_path)

dbutils.fs.rm(output_path, true)

df.write.mode("overwrite").format("parquet").save(output_path)