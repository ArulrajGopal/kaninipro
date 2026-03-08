import pandas as pd
from databricks import sql


server_hostname = "your_server_hostname_here"
http_path = "your_http_path_here"
access_token = "your_access_token_here"


with sql.connect(
    server_hostname=server_hostname,
    http_path=http_path,
    access_token=access_token
) as conn:

    df = pd.read_sql("SELECT * FROM kaninipro_catalog.dev.sample_table limit 5", conn)

print(df)