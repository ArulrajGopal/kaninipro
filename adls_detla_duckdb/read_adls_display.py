import duckdb
import os 

# con = duckdb.connect()
# con.execute("INSTALL delta;")
# con.execute("LOAD delta;")

# con.execute("INSTALL azure;")
# con.execute("LOAD azure;")

# con.execute(f"""
#         CREATE SECRET azure_spn (
#             TYPE azure,
#             PROVIDER service_principal,
#             TENANT_ID 'xxxx',
#             CLIENT_ID 'xxxx',
#             CLIENT_SECRET 'xxx',
#             ACCOUNT_NAME 'xxx'
# );
# """)

# query_1 = """
#     SELECT *
#     FROM delta_scan('abfss://data@kaninipro.dfs.core.windows.net/target/people_delta/')
#     where first_name <> 'first_name'
#     LIMIT 10
# """
# # 'az://kaninipro.blob.core.windows.net/data/target/people_delta/'
# # 'abfss://data@kaninipro.dfs.core.windows.net/target/people_delta/'

# df = con.execute(query_1).df()
# print(df)






