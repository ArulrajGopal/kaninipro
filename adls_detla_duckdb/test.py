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

query = """
    select count(*) from (    SELECT distinct loaded_dt
    FROM delta_scan('abfss://data@kaniniproraw.dfs.core.windows.net/test_data/sensor_data/'))
"""

df = con.execute(query).df()
print(df)






