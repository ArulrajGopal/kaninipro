# Databricks notebook source
spark.sql("""
CREATE OR REPLACE TABLE kaninipro.dev.group_row_level_security (
    group_name STRING,
    continent  STRING
)
""")

spark.sql("""
INSERT INTO kaninipro.dev.group_row_level_security (group_name, continent)
VALUES
    ('north_america_team', 'North America'),
    ('asia_team',          'Asia')
""")

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE FUNCTION kaninipro.dev.continent_group_filter (continent STRING)
RETURNS BOOLEAN
LANGUAGE SQL
RETURN
exists(
select 1
from kaninipro.dev.group_row_level_security grls
where grls.continent = continent_group_filter.continent
and is_account_group_member(grls.group_name)
)
""")

spark.sql("""
ALTER TABLE kaninipro.dev.sales_customers SET ROW FILTER kaninipro.dev.continent_group_filter ON (continent)
""")

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended kaninipro.dev.sales_customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from kaninipro.dev.sales_customers

# COMMAND ----------



# COMMAND ----------

