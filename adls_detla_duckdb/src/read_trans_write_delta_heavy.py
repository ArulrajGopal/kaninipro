import duckdb
import os 
from datetime import datetime

con = duckdb.connect()
con.execute("INSTALL delta;")
con.execute("LOAD delta;")

con.execute("INSTALL azure;")
con.execute("LOAD azure;")

tenant_id = os.getenv("AZ_TENANT_ID")
client_id = os.getenv("AZ_CLIENT_ID")
client_secret = os.getenv("AZ_CLIENT_SECRET")
storage_ac_name = os.getenv("AZ_STORAGE_AC_NAME")


con.execute(f"""
        CREATE SECRET azure_spn (
            TYPE azure,
            PROVIDER service_principal,
            TENANT_ID '{tenant_id}',
            CLIENT_ID '{client_id}',
            CLIENT_SECRET '{client_secret}',
            ACCOUNT_NAME '{storage_ac_name}'
);
""")

# agg_query = """
#     select 
#     sum(sensor_a) as sum_sen_a,
#     sum(sensor_b) as sum_sen_b,
#     sum(sensor_c) as sum_sen_c,
#     sum(sensor_d) as sum_sen_d,
#     sum(sensor_e) as sum_sen_e,
#     sum(sensor_f) as sum_sen_f,
#     sum(sensor_g) as sum_sen_g,
#     sum(sensor_h) as sum_sen_h
#     from delta_scan('abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data/')
#     group by unit_id
# """
# con.execute("""
#     COPY (
#         SELECT *
#         FROM delta_scan(
#             'abfss://data@kaniniproraw.dfs.core.windows.net/people_delta/'
#         )
#         WHERE first_name <> 'first_name'
#           AND id IN (3, 4)
#     )
#     TO 'abfss://data@kaniniproraw.dfs.core.windows.net/people_delta_filtered/people.parquet'
#     (FORMAT parquet)
# """)

start_time = datetime.now()
print("started at ", start_time)

con.execute("""
    COPY (
        SELECT 
        unit_id,
        sum(sensor_a) as sum_sen_a,
        sum(sensor_b) as sum_sen_b,
        sum(sensor_c) as sum_sen_c,
        sum(sensor_d) as sum_sen_d,
        sum(sensor_e) as sum_sen_e,
        sum(sensor_f) as sum_sen_f,
        sum(sensor_g) as sum_sen_g,
        sum(sensor_h) as sum_sen_h
        FROM parquet_scan('abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data/loaded_dt=20260207201903/*.parquet')
        group by unit_id
    )
    TO 'abfss://data@kaniniproraw.dfs.core.windows.net/sensor_data_output/sens_parquet.parquet'
    (FORMAT parquet)
""")



end_time = datetime.now()
print("end_time: ", start_time)
print("Time taken:", end_time - start_time)
print("Successfully completed")









