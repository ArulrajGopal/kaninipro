# Databricks notebook source
# Unity Catalog — Python Function
# Stored persistently in the catalog. Runs Python logic server-side via DBR 13.3+.

# COMMAND ----------

spark.sql("""
    CREATE OR REPLACE FUNCTION kaninipro.dev.salary_band_py(salary DOUBLE)
    RETURNS INT
    LANGUAGE PYTHON
    COMMENT 'Returns salary band: 3=high, 2=mid, 1=low, -1=null'
    AS $$
        if salary is None:
            return -1
        if salary >= 100000:
            return 3
        elif salary >= 75000:
            return 2
        return 1
    $$
""")

# COMMAND ----------

# Call via DataFrame API
df = spark.table("kaninipro.dev.employees")

result_df = df.selectExpr(
    "id",
    "kaninipro.dev.salary_band_py(salary) AS salary_band"
)

result_df.display()

# COMMAND ----------

# Call via spark.sql
result_df2 = spark.sql("""
    SELECT
        id,
        salary,
        kaninipro.dev.salary_band_py(salary) AS salary_band
    FROM kaninipro.dev.employees
""")

result_df2.display()

# COMMAND ----------

# Grant execute privilege
spark.sql("""
    GRANT EXECUTE ON FUNCTION kaninipro.dev.salary_band_py
    TO `data-analysts`
""")

# COMMAND ----------

# Inspect the stored function
spark.sql("DESCRIBE FUNCTION EXTENDED kaninipro.dev.salary_band_py").display()
