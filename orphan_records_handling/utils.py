import psycopg2
import os 
from sqlalchemy import create_engine
from config import *


def run_sql_script(sql_path):

    # Connect to the database
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

    try:
        with conn:
            with conn.cursor() as cur:
                with open(sql_path, "r") as sql_file:
                    sql_script = sql_file.read()

                cur.execute(sql_script)
                print("SQL file executed successfully.")

    finally:
        conn.close()


def load_to_sql(df, table_name):
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"data loaded in {table_name} successfully.")


def run_stored_proc(stored_procedure_name):
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"CALL {stored_procedure_name}()")
                print(f"{stored_procedure_name} executed successfully.")
                
    finally:
        conn.close()






