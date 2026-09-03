# Databricks notebook source
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
    force=True,
)

logging.debug("Row-level detail: batch_id=42")
logging.info("LOGGING (invisible right now): Job starting...")
logging.warning("Retry #1 after transient timeout")
logging.error("Failed to write partition 7")
logging.critical("ETL job failed: unrecoverable error")


logging.basicConfig(
    level=logging.CRITICAL + 1,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)

logger = logging.getLogger("etl_job")

logger.debug("Row-level detail: batch_id=42")
logger.info("Batch 42 started")
logger.warning("Retry #1 after transient timeout")
logger.error("Failed to write partition 7")
logger.critical("ETL job failed: unrecoverable error")

# COMMAND ----------

