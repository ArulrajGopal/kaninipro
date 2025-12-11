# Resource Configuration
resource_group_name = "rg-databricks-metastore"
location            = "East US"

# Storage Account Configuration (must be globally unique)
storage_account_name  = "dbmetastore123456"
metastore_container_name = "metastore"

# Managed Identity Configuration
managed_identity_name = "databricks-identity"

# Databricks Workspace Configuration
workspace_name = "databricks-workspace"
databricks_sku = "premium"

# Metastore Configuration
metastore_name           = "primary-metastore"
storage_credential_name  = "metastore-credential"
access_connector_name    = "databricks-access-connector"

# Unity Catalog Configuration
unity_catalog_name = "arul_catalog"
schema_name        = "default_schema"

# Tags
tags = {
  Environment = "Production"
  ManagedBy   = "Terraform"
  Application = "Databricks"
  CostCenter  = "Engineering"
}
