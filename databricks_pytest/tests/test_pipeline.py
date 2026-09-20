"""Integration tests for the end-to-end orders pipeline."""

from src.pipeline import build_enriched_orders, transform_and_write


def test_build_enriched_orders_end_to_end(raw_orders_df, customers_df):
    result = build_enriched_orders(raw_orders_df, customers_df)
    rows = {r.order_id: r for r in result.collect()}

    # duplicate order_id was collapsed and null order_id dropped
    assert set(rows.keys()) == {"o1", "o2", "o3", "o5"}

    # transformations were applied in order: clean -> dedupe -> total -> category -> join
    assert rows["o1"].product == "WIDGET"
    assert rows["o1"].total_amount == 100.0
    assert rows["o1"].order_category == "MEDIUM"
    assert rows["o1"].region == "EAST"


def test_transform_and_write_writes_expected_outputs(spark, raw_orders_df, customers_df, tmp_path):
    """Validates the write step using in-memory DataFrames as input - no file-based
    orders/customers source is involved, since orders are only ever loaded via
    Auto Loader in the real pipeline (not something local tests can exercise)."""
    output_dir = tmp_path / "output"

    transform_and_write(raw_orders_df, customers_df, output_path=str(output_dir))

    enriched = spark.read.parquet(str(output_dir / "enriched_orders"))
    revenue = spark.read.parquet(str(output_dir / "revenue_by_customer"))

    # raw_orders_df has 6 rows: one null order_id dropped, one duplicate order_id collapsed -> 4 remain
    assert enriched.count() == 4
    assert {r.order_id for r in enriched.collect()} == {"o1", "o2", "o3", "o5"}
    assert {r.region for r in enriched.collect()} == {"EAST", "WEST", "CENTRAL"}

    revenue_by_customer = {r.customer_id: r.total_revenue for r in revenue.collect()}
    assert revenue_by_customer == {"c1": 400.0, "c2": 20.0, "c3": 0.0}
