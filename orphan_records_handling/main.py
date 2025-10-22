import psycopg2
import os 
import utils
import pandas as pd
import sys


BASE_DIR = os.path.dirname(__file__)

#run sql script for creating tables
sql_path = f"{BASE_DIR}/createStatement.sql"

utils.run_sql_script(sql_path)


batch_no = sys.argv[1]
storage_account = "arulrajgopalshare"
container = "kaniniwitharul"



#reading the data from blob storage
orders_url = f"https://{storage_account}.blob.core.windows.net/{container}/orphan_records_handling/{batch_no}/orders.csv"
order_items_url = f"https://{storage_account}.blob.core.windows.net/{container}/orphan_records_handling/{batch_no}/order_items.csv"

orders_df = pd.read_csv(orders_url)
order_items_df = pd.read_csv(order_items_url)


orders_df['order_date'] = pd.to_datetime(orders_df['order_date'], format='%Y-%m-%d').dt.date


#loading into sql stage tables
utils.load_to_sql(order_items_df,"order_items_stage")
utils.load_to_sql(orders_df,"orders_stage")


#executing stored procedures
utils.run_stored_proc("load_orders")
utils.run_stored_proc("load_order_items")
utils.run_stored_proc("load_order_details")





