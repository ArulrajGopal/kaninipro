# Databricks notebook source
# Unity Catalog — SQL Function
# Stored persistently in the catalog. No Python runtime involved.

# COMMAND ----------

spark.sql("""
    CREATE OR REPLACE FUNCTION kaninipro.dev.salary_band(salary DOUBLE)
    RETURNS INT
    LANGUAGE SQL
    COMMENT 'Returns salary band: 3=high, 2=mid, 1=low, -1=null'
    RETURN
        CASE
            WHEN salary IS NULL     THEN -1
            WHEN salary >= 100000   THEN 3
            WHEN salary >= 75000    THEN 2
            ELSE 1
        END
""")

# COMMAND ----------

# Call via DataFrame API (three-part name: catalog.schema.function)
df = spark.table("kaninipro.dev.employees")

result_df = df.selectExpr(
    "id",
    "kaninipro.dev.salary_band(salary) AS salary_band"
)

result_df.display()

# COMMAND ----------

# Call via spark.sql — works from any notebook or SQL warehouse with EXECUTE privilege
result_df2 = spark.sql("""
    SELECT
        id,
        salary,
        kaninipro.dev.salary_band(salary) AS salary_band
    FROM kaninipro.dev.employees
""")

result_df2.display()

# COMMAND ----------

# Grant execute privilege to another user / group / service principal
spark.sql("""
    GRANT EXECUTE ON FUNCTION kaninipro.dev.salary_band
    TO `data-analysts`
""")

# COMMAND ----------

# Inspect the function definition stored in Unity Catalog
spark.sql("DESCRIBE FUNCTION EXTENDED kaninipro.dev.salary_band").display()
