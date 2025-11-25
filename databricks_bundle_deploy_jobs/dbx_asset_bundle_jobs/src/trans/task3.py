# Databricks notebook source
import json

env = dbutils.widgets.get("env")


config_path = "../config/my_project.json"
with open(config_path, "r") as f:
    config = json.load(f).get(env, {})

# COMMAND ----------

storage_account = config["storage_account"]
emp_dept_path = config["employee_department_target"]
emp_sal_path = config["employee_salary_target"]
agg_path = config["final_aggregated_path"]


adls_key = dbutils.secrets.get(scope="myscope", key="adls_key")
spark.conf.set(f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",adls_key)

# COMMAND ----------

emp_dept_df =spark.read.format("parquet").load(emp_dept_path)
emp_sal_df =spark.read.format("parquet").load(emp_sal_path)

# COMMAND ----------

joined_df = emp_dept_df.join(emp_sal_df, "id")

agg_df = joined_df.groupBy("department").agg({"salary": "avg"})


# COMMAND ----------

agg_df.write.mode("overwrite").format("parquet").save(agg_path)