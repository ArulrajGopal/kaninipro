# Databricks notebook source
# MAGIC %sql
# MAGIC select * from kaninipro.dev.sales_customers

# COMMAND ----------

spark.sql("""
    CREATE OR REPLACE FUNCTION kaninipro.dev.mask_pii(col STRING)
    RETURNS STRING
    LANGUAGE SQL
    RETURN (
        CASE 
            WHEN is_member('grp_2') THEN col 
            ELSE '**********' 
        END
    )
""")

spark.sql("""
    ALTER TABLE kaninipro.dev.sales_customers 
    ALTER COLUMN phone_number 
    SET MASK kaninipro.dev.mask_pii
""")

spark.sql("""
    ALTER TABLE kaninipro.dev.sales_customers 
    ALTER COLUMN address 
    SET MASK kaninipro.dev.mask_pii
""")

spark.sql("""
    ALTER TABLE kaninipro.dev.sales_customers 
    ALTER COLUMN email_address 
    SET MASK kaninipro.dev.mask_pii
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended kaninipro.dev.sales_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro.dev.sales_customers

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

