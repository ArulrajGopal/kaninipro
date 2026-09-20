# Databricks notebook source
# MAGIC %md
# MAGIC # Orders ETL - Test Suite
# MAGIC Runs the pytest suite (`tests/`) on a Databricks cluster, so tests run
# MAGIC against the runtime's real Spark + Java instead of requiring a local
# MAGIC PySpark/Java install. Triggered via `resources/orders_etl_test_job.yml`
# MAGIC (`databricks bundle run orders_etl_test_job`).
# MAGIC
# MAGIC Tests always use the sample data in `data/` and the in-memory fixtures
# MAGIC in `tests/conftest.py` — never the ADLS/Auto Loader source used by the
# MAGIC real pipeline job (`orders_etl_job`).

# COMMAND ----------

# MAGIC %pip install pytest==8.2.0 chispa==0.10.1
dbutils.library.restartPython()

# COMMAND ----------

import os
import sys

# Workspace Files (where the bundle syncs the repo) doesn't support the
# directory-create operation Python needs to write __pycache__, which makes
# conftest.py fail to import with OSError: [Errno 95] Operation not
# supported. Disable bytecode caching so pytest never tries.
sys.dont_write_bytecode = True

# The bundle syncs the whole repo, so the notebook's parent directory is the
# repo root — add it to the path to import the `src` and `tests` packages.
repo_root = os.path.abspath("..")
sys.path.append(repo_root)

# COMMAND ----------

import pytest

exit_code = pytest.main(["-v", os.path.join(repo_root, "tests")])
assert exit_code == 0, f"pytest reported failures (exit code: {exit_code})"
