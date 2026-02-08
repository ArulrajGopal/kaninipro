import duckdb
import os 

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

count_query = """
    select count(*) from delta_scan('abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data/')
"""

agg_query = """
    select 
    sum(sensor_a) as sum_sen_a,
    sum(sensor_b) as sum_sen_b,
    sum(sensor_c) as sum_sen_c,
    sum(sensor_d) as sum_sen_d,
    sum(sensor_e) as sum_sen_e,
    sum(sensor_f) as sum_sen_f,
    sum(sensor_g) as sum_sen_g,
    sum(sensor_h) as sum_sen_h
    from delta_scan('abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data/')
    group by unit_id
"""

df = con.execute(agg_query).df()
print(df)

# total count 6,250,000,000






