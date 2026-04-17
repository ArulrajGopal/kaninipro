# Resource Group
resource "azurerm_resource_group" "rgadls" {
  name     = var.adls_resource_group_name 
  location = var.location
  tags     = var.tags
}


# Storage Account for Metastore
resource "azurerm_storage_account" "metastore" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rgadls.name
  location                 = azurerm_resource_group.rgadls.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  https_traffic_only_enabled = true
  is_hns_enabled           = true

  tags = var.tags

  depends_on = [azurerm_resource_group.rgadls]
}

# Storage Container for Metastore
resource "azurerm_storage_container" "metastore_container" {
  name                  = var.metastore_container_name
  storage_account_name  = azurerm_storage_account.metastore.name
  container_access_type = "private"

  depends_on = [azurerm_storage_account.metastore]
}
