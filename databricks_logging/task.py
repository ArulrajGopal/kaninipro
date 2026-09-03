# Databricks notebook source
import os
import time
import logging

# COMMAND ----------

dbutils.widgets.text("log_level", "INFO")
dbutils.widgets.text("run_id", "local")
dbutils.widgets.text("job_id", "local")
log_level_param = dbutils.widgets.get("log_level").upper()
log_level = getattr(logging, log_level_param, logging.INFO)

# COMMAND ----------

def get_databricks_job_run_id():
    return dbutils.widgets.get("run_id"), dbutils.widgets.get("job_id")

run_id, job_id = get_databricks_job_run_id()

# COMMAND ----------

# --- UC Volume log path ---
volume_log_dir = "/Volumes/kaninipro_catalog/dev/log"
# optional: keep logs organized under a subfolder + timestamped file per run, tagged with run_id
log_file_path = os.path.join(
    volume_log_dir,
    f"employees_etl_{time.strftime('%Y%m%d_%H%M%S')}_job{job_id}_run{run_id}.log"
)

# --- Logger setup ---
logger = logging.getLogger("employees_etl")
logger.setLevel(log_level)

if not logger.handlers:
    formatter = logging.Formatter(
        f"%(asctime)s %(levelname)s %(name)s [run_id={run_id}]: %(message)s"
    )

    # File handler -> writes into UC managed volume
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # (optional) keep console output too, useful when viewing driver logs
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)


# COMMAND ----------

logger.info(f"Logger initialized at level {log_level_param}, run_id={run_id}, writing to {log_file_path}")

# --- Sample data ---
logger.info("Creating sample DataFrame")

data = [
    (1, "Alice", "Engineering"),
    (2, "Bob", "Marketing"),
    (3, "Charlie", "Sales"),
    (4, "Smith", None)
]
columns = ["id", "name", "department"]

df = spark.createDataFrame(data, columns)


if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"DataFrame created: {df.count()} rows, {len(df.columns)} columns")
    logger.debug(f"Schema: {df.schema.simpleString()}")


null_department_count = df.filter(df.department.isNull()).count()
if null_department_count > 0:
    logger.warning(f"Found {null_department_count} record(s) with null 'department' field")


table_name = "kaninipro_catalog.dev.employees"
logger.info(f"Writing DataFrame to table: {table_name}")
start_time = time.time()

try:
    df.write \
        .mode("overwrite") \
        .saveAsTable(table_name)

    elapsed = time.time() - start_time
    logger.info(f"Successfully wrote to {table_name} in {elapsed:.2f}s")

except Exception as e:
    logger.error(f"Failed to write to {table_name}: {e}")
    raise


# COMMAND ----------

for h in logger.handlers[:]:
    h.flush()
    h.close()
    logger.removeHandler(h)