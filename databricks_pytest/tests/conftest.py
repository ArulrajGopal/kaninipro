"""Shared pytest fixtures for the orders ETL test suite."""

from datetime import datetime

import pytest
from pyspark.sql import SparkSession

from src.schemas import CUSTOMERS_SCHEMA, ORDERS_SCHEMA


@pytest.fixture(scope="session")
def spark():
    """Session-scoped SparkSession, reused across all tests.

    Databricks serverless compute pre-configures a Spark Connect session
    (via SPARK_REMOTE); forcing a local master here conflicts with it, so
    just reuse whatever session the runtime already provides (Spark
    Connect on serverless, classic Spark on a job cluster).
    """
    yield (
        SparkSession.builder.appName("pytest-orders-etl")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )


@pytest.fixture
def raw_orders_df(spark):
    """Deliberately messy orders data: nulls, duplicates, mixed-case product names."""
    data = [
        ("o1", "c1", " widget ", 5, 20.0, datetime(2024, 1, 1)),
        ("o1", "c1", " widget ", 5, 20.0, datetime(2024, 1, 2)),  # duplicate order_id, newer date
        ("o2", "c1", "Gadget", 2, 150.0, datetime(2024, 1, 3)),
        ("o3", "c2", "widget", 1, 20.0, datetime(2024, 1, 2)),
        (None, "c2", "gizmo", 10, 60.0, datetime(2024, 1, 5)),  # missing order_id, dropped
        ("o5", "c3", "gadget", None, None, datetime(2024, 1, 6)),  # missing qty/price -> 0
    ]
    return spark.createDataFrame(data, schema=ORDERS_SCHEMA)


@pytest.fixture
def customers_df(spark):
    data = [
        ("c1", "Acme Corp", "EAST"),
        ("c2", "Globex Inc", "WEST"),
        ("c3", "Initech", "CENTRAL"),
    ]
    return spark.createDataFrame(data, schema=CUSTOMERS_SCHEMA)
