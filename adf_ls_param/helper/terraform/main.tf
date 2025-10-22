provider "azurerm" {
  features {}

  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}


provider "azuread" {
 tenant_id       = var.tenant_id
 client_id       = var.client_id
 client_secret   = var.client_secret
}


resource "azurerm_resource_group" "resource_group" {
  name     = "test_resource_group"
  location = "South India"
}

resource "azurerm_storage_account" "source" {
  name                     = "sourceadls6789"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = "Terraform"
  }

  
}

resource "azurerm_storage_account" "target1" {
  name                     = "target1adls6789"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = "Terraform"
  }
}

resource "azurerm_storage_account" "target2" {
  name                     = "target2adls6789"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true


  tags = {
    environment = "Terraform"
  }
}


# Add Azure Data Factory (ADF)
resource "azurerm_data_factory" "adf" {
  name                = "azuredatafactory6789"
  location            = azurerm_resource_group.resource_group.location
  resource_group_name = azurerm_resource_group.resource_group.name

  tags = {
    environment = "Terraform"
  }
}


data "azuread_client_config" "current" {}

resource "azuread_application" "ad_app" {
  display_name = "spn6789"
  owners       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal" "spn" {
  client_id                    = azuread_application.ad_app.client_id
  app_role_assignment_required = false
  owners                       = [data.azuread_client_config.current.object_id]
}

resource "azurerm_role_assignment" "spn_blob_contributor" {
  scope                = azurerm_resource_group.resource_group.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.spn.object_id
}




