# output "databricks_workspace_url" {
#   value       = azurerm_databricks_workspace.workspace.workspace_url
#   description = "The URL for the Databricks workspace"
# }

# output "databricks_workspace_id" {
#   value       = azurerm_databricks_workspace.workspace.workspace_id
#   description = "The ID of the Databricks workspace"
# }

# output "metastore_id" {
#   value       = databricks_metastore.metastore.metastore_id
#   description = "The ID of the Databricks metastore"
# }

# output "metastore_storage_path" {
#   value       = databricks_metastore.metastore.storage_root
#   description = "The root storage path for the metastore"
# }

# output "storage_account_name" {
#   value       = azurerm_storage_account.metastore.name
#   description = "The name of the storage account for metastore"
# }

# output "storage_account_id" {
#   value       = azurerm_storage_account.metastore.id
#   description = "The resource ID of the storage account"
# }

# output "managed_identity_id" {
#   value       = azurerm_user_assigned_identity.databricks_identity.id
#   description = "The ID of the managed identity used for storage access"
# }

# output "managed_identity_principal_id" {
#   value       = azurerm_user_assigned_identity.databricks_identity.principal_id
#   description = "The principal ID of the managed identity"
# }

# output "unity_catalog_name" {
#   value       = databricks_catalog.main.name
#   description = "The name of the Unity Catalog"
# }

# output "catalog_schema_name" {
#   value       = databricks_schema.default_schema.name
#   description = "The name of the default schema"
# }

# output "resource_group_name" {
#   value       = azurerm_resource_group.rg.name
#   description = "The name of the resource group"
# }
