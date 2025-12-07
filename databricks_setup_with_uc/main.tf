# azurerm provider setup
provider "azurerm" {
  features {}

  tenant_id       = var.tenant_id
  subscription_id = var.subscriber_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

# resource group and storage account

resource "azurerm_resource_group" "resource_group" {
  name     = "test_resource_group"
  location = "South India"
}

resource "azurerm_storage_account" "storage_account_dev" {
  name                     = "kaniniproadlsdev"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = "Terraform"
  }
}


# databricks workspace

resource "azurerm_resource_group" "rg_dev" {
  name     = "dbx-dev"
  location = "South India"
}


resource "azurerm_databricks_workspace" "dbx1" {
  name                = "kaninipro-dbx1-dev"
  resource_group_name = azurerm_resource_group.rg_dev.name
  location            = azurerm_resource_group.rg_dev.location
  sku                 = "premium"

    tags = {
    environment = "Terraform"
  }
}


