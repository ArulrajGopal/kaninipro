# azurerm provider setup
provider "azurerm" {
  features {}

  tenant_id       = var.tenant_id
  subscription_id = var.subscriber_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

# Create Resource Group
resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
}

# Create Storage Account
resource "azurerm_storage_account" "this" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
  
  tags = {
    environment = var.environment
  }
}

# Create Storage Container
resource "azurerm_storage_container" "this" {
  name                  = var.storage_container_name
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}

# Create Databricks Access Connector
resource "azurerm_databricks_access_connector" "this" {
  name                = var.access_connector_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  
  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = var.environment
  }
}

# Create Databricks Workspace
resource "azurerm_databricks_workspace" "this" {
  name                = var.workspace_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = var.databricks_sku
  
  tags = {
    environment = var.environment
  }

  depends_on = [
    azurerm_role_assignment.access_connector_storage_blob_contributor
  ]
}

# Grant Storage Blob Data Contributor access to Access Connector
resource "azurerm_role_assignment" "access_connector_storage_blob_contributor" {
  scope              = azurerm_storage_account.this.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id       = azurerm_databricks_access_connector.this.identity[0].principal_id
}

# Output values
output "resource_group_id" {
  value       = azurerm_resource_group.this.id
  description = "The ID of the created resource group"
}

output "storage_account_id" {
  value       = azurerm_storage_account.this.id
  description = "The ID of the created storage account"
}

output "storage_account_name" {
  value       = azurerm_storage_account.this.name
  description = "The name of the created storage account"
}

output "databricks_workspace_id" {
  value       = azurerm_databricks_workspace.this.id
  description = "The ID of the created Databricks workspace"
}

output "databricks_workspace_url" {
  value       = azurerm_databricks_workspace.this.workspace_url
  description = "The Databricks workspace URL"
}

output "access_connector_id" {
  value       = azurerm_databricks_access_connector.this.id
  description = "The ID of the Access Connector"
}

output "access_connector_principal_id" {
  value       = azurerm_databricks_access_connector.this.identity[0].principal_id
  description = "The principal ID of the Access Connector managed identity"
}

