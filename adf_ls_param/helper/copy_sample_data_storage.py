# pip install pandas azure-identity azure-storage-blob

# import lib
import pandas as pd
from io import StringIO
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceExistsError


# Read sample data from URL
sample_data_url = f"https://arulrajgopalshare.blob.core.windows.net/kaniniwitharul/adf_ls_param/sample_data.csv"
sample_data_df = pd.read_csv(sample_data_url)


# Convert DataFrame to CSV in memory
csv_buffer = StringIO()
sample_data_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

# Azure credentials
tenant_id       = "<your-tenant-id>"
client_id       = "<your-client-id>"
client_secret   = "<your-client-secret>"



# Storage account details
storage_account_name = "sourceadls6789"
container_name = "input"
blob_name = "sample_data.csv"

# Authenticate
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Create BlobServiceClient using the credential
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)


try:
    blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except ResourceExistsError:
    print(f"Container '{container_name}' already exists.")

    

# Upload to blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_client.upload_blob(csv_data, overwrite=True)

print("Upload complete.")


