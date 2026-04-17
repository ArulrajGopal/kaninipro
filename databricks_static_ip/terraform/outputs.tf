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


output "nat_gateway_public_ip" {
  value = azurerm_public_ip.nat_ip.ip_address
}