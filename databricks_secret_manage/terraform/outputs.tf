output "databricks_workspace_url" {
  value       = azurerm_databricks_workspace.workspace.workspace_url
  description = "The URL for the Databricks workspace"
}

output "databricks_workspace_id" {
  value       = azurerm_databricks_workspace.workspace.workspace_id
  description = "The ID of the Databricks workspace"
}

output "storage_account_name" {
  value       = azurerm_storage_account.metastore.name
  description = "The name of the storage account for metastore"
}

output "current_client_config" {
  value = {
    client_id       = data.azurerm_client_config.current.client_id
    tenant_id       = data.azurerm_client_config.current.tenant_id
    subscription_id = data.azurerm_client_config.current.subscription_id
    object_id       = data.azurerm_client_config.current.object_id
  }
  description = "The current Azure client config used by Terraform"
}
