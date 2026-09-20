"""Unit tests for individual PySpark transformation functions."""

from datetime import datetime

from chispa.dataframe_comparer import assert_df_equality

from src.schemas import ORDERS_SCHEMA
from src.transformations import (
    add_order_total,
    aggregate_revenue_by_customer,
    categorize_orders,
    clean_orders,
    deduplicate_orders,
    filter_high_value_customers,
    join_customer_region,
)


def test_clean_orders_drops_nulls_and_normalizes_product(raw_orders_df):
    result = clean_orders(raw_orders_df)
    rows = {r.order_id for r in result.collect()}

    # the row with a null order_id must be dropped
    assert None not in rows
    assert rows == {"o1", "o2", "o3", "o5"}

    # product names are trimmed and upper-cased
    products = {r.order_id: r.product for r in result.collect()}
    assert products["o1"] == "WIDGET"
    assert products["o2"] == "GADGET"

    # missing quantity/unit_price are coalesced to 0
    o5 = next(r for r in result.collect() if r.order_id == "o5")
    assert o5.quantity == 0
    assert o5.unit_price == 0.0


def test_deduplicate_orders_keeps_most_recent(raw_orders_df):
    cleaned = clean_orders(raw_orders_df)
    result = deduplicate_orders(cleaned)

    order_ids = [r.order_id for r in result.collect()]
    assert sorted(order_ids) == ["o1", "o2", "o3", "o5"]
    assert len(order_ids) == len(set(order_ids))  # no duplicates remain

    o1 = next(r for r in result.collect() if r.order_id == "o1")
    assert o1.order_date == datetime(2024, 1, 2)  # the newer of the two duplicate rows


def test_add_order_total_computes_quantity_times_price(spark):
    data = [("o1", "c1", "WIDGET", 5, 20.0, datetime(2024, 1, 1))]
    df = spark.createDataFrame(data, schema=ORDERS_SCHEMA)

    result = add_order_total(df).select("order_id", "total_amount")
    expected = spark.createDataFrame([("o1", 100.0)], schema="order_id string, total_amount double")

    assert_df_equality(result, expected, ignore_row_order=True)


def test_categorize_orders_buckets_by_total_amount(spark):
    data = [
        ("o1", "c1", "A", 1, 50.0, datetime(2024, 1, 1)),  # 50 -> LOW
        ("o2", "c1", "B", 1, 150.0, datetime(2024, 1, 1)),  # 150 -> MEDIUM
        ("o3", "c1", "C", 1, 600.0, datetime(2024, 1, 1)),  # 600 -> HIGH
    ]
    df = spark.createDataFrame(data, schema=ORDERS_SCHEMA)

    result = categorize_orders(add_order_total(df))
    categories = {r.order_id: r.order_category for r in result.collect()}

    assert categories == {"o1": "LOW", "o2": "MEDIUM", "o3": "HIGH"}


def test_join_customer_region_enriches_orders(raw_orders_df, customers_df):
    cleaned = deduplicate_orders(clean_orders(raw_orders_df))
    result = join_customer_region(cleaned, customers_df)

    regions = {r.order_id: r.region for r in result.collect()}
    assert regions["o1"] == "EAST"
    assert regions["o3"] == "WEST"
    assert regions["o5"] == "CENTRAL"


def test_aggregate_revenue_by_customer(raw_orders_df, customers_df):
    enriched = categorize_orders(
        add_order_total(deduplicate_orders(clean_orders(raw_orders_df)))
    )
    result = aggregate_revenue_by_customer(enriched)
    revenue = {r.customer_id: r.total_revenue for r in result.collect()}
    counts = {r.customer_id: r.order_count for r in result.collect()}

    assert revenue == {"c1": 400.0, "c2": 20.0, "c3": 0.0}
    assert counts == {"c1": 2, "c2": 1, "c3": 1}


def test_filter_high_value_customers(spark):
    data = [("c1", 400.0, 2), ("c2", 20.0, 1), ("c3", 5000.0, 3)]
    agg_df = spark.createDataFrame(
        data, schema="customer_id string, total_revenue double, order_count long"
    )

    result = filter_high_value_customers(agg_df, threshold=100.0)
    customer_ids = {r.customer_id for r in result.collect()}

    assert customer_ids == {"c1", "c3"}
