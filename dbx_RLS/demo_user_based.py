# Databricks notebook source
spark.sql("""
CREATE OR REPLACE TABLE kaninipro.dev.row_level_security (
    user_email STRING,
    continent STRING
)
""")

spark.sql("""
INSERT INTO kaninipro.dev.row_level_security (user_email, continent)
VALUES
    ('user-1@arulrajgopaloutlook.onmicrosoft.com', 'North America')
""")

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE FUNCTION kaninipro.dev.continent_filter (continent STRING)
RETURNS BOOLEAN
LANGUAGE SQL
RETURN
exists(
select 1
from kaninipro.dev.row_level_security rls
where rls.continent = continent_filter.continent
and rls.user_email = current_user()
)
""")

spark.sql("""
ALTER TABLE kaninipro.dev.sales_customers SET ROW FILTER kaninipro.dev.continent_filter ON (continent)
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended kaninipro.dev.sales_customers;

# COMMAND ----------

