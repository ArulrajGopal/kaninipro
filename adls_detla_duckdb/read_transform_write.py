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


con.execute("""
    COPY (
        SELECT *
        FROM delta_scan(
            'abfss://data@kaninipro.dfs.core.windows.net/target/people_delta/'
        )
        WHERE first_name <> 'first_name'
          AND id IN (3, 4)
    )
    TO 'abfss://data@kaninipro.dfs.core.windows.net/target/people_delta_filtered/people.parquet'
    (FORMAT parquet)
""")

print("successfully written into parquet !!!")