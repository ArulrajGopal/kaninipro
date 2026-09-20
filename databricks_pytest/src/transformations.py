"""Reusable PySpark transformations for the orders ETL pipeline."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def clean_orders(df: DataFrame) -> DataFrame:
    """Drop rows missing required keys and normalize product names."""
    return (
        df.filter(F.col("order_id").isNotNull())
        .filter(F.col("customer_id").isNotNull())
        .withColumn("product", F.trim(F.upper(F.col("product"))))
        .withColumn("quantity", F.coalesce(F.col("quantity"), F.lit(0)))
        .withColumn("unit_price", F.coalesce(F.col("unit_price"), F.lit(0.0)))
    )


def deduplicate_orders(df: DataFrame) -> DataFrame:
    """Keep only the most recent row per order_id."""
    window = Window.partitionBy("order_id").orderBy(F.col("order_date").desc())
    return (
        df.withColumn("_row_num", F.row_number().over(window))
        .filter(F.col("_row_num") == 1)
        .drop("_row_num")
    )


def add_order_total(df: DataFrame) -> DataFrame:
    """Add a total_amount column computed from quantity * unit_price."""
    return df.withColumn("total_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))


def categorize_orders(df: DataFrame) -> DataFrame:
    """Bucket orders into LOW / MEDIUM / HIGH value categories."""
    return df.withColumn(
        "order_category",
        F.when(F.col("total_amount") >= 500, "HIGH")
        .when(F.col("total_amount") >= 100, "MEDIUM")
        .otherwise("LOW"),
    )


def join_customer_region(orders_df: DataFrame, customers_df: DataFrame) -> DataFrame:
    """Enrich orders with the customer's region."""
    return orders_df.join(
        customers_df.select("customer_id", "customer_name", "region"),
        on="customer_id",
        how="left",
    )


def aggregate_revenue_by_customer(df: DataFrame) -> DataFrame:
    """Summarize total revenue and order count per customer."""
    return df.groupBy("customer_id").agg(
        F.sum("total_amount").alias("total_revenue"),
        F.count("order_id").alias("order_count"),
    )


def filter_high_value_customers(agg_df: DataFrame, threshold: float = 1000.0) -> DataFrame:
    """Return only customers whose total revenue meets the threshold."""
    return agg_df.filter(F.col("total_revenue") >= threshold)
