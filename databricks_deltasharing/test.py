import delta_sharing

profile_file = "config.share"
share_name = "data_share"
schema_name = "dev"
table_name = "sample_table"


table_url = f"{profile_file}#{share_name}.{schema_name}.{table_name}"

df = delta_sharing.load_as_pandas(table_url)

print(df.head())
