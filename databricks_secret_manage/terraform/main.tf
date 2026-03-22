terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "azurerm" {
  features {}
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}


provider "databricks" {
  alias      = "account"
  host       = "https://accounts.cloud.databricks.com"
  account_id = var.account_id

  azure_tenant_id     = var.tenant_id
  azure_client_id     = var.client_id
  azure_client_secret = var.client_secret
}


# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# Storage Account for Metastore
resource "azurerm_storage_account" "metastore" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  https_traffic_only_enabled = true
  is_hns_enabled           = true

  tags = var.tags

  depends_on = [azurerm_resource_group.rg]
}

# Storage Container for Metastore
resource "azurerm_storage_container" "metastore_container" {
  name                  = var.metastore_container_name
  storage_account_name  = azurerm_storage_account.metastore.name
  container_access_type = "private"

  depends_on = [azurerm_storage_account.metastore]
}

# Databricks Workspace
resource "azurerm_databricks_workspace" "workspace" {
  name                = var.workspace_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = var.databricks_sku

  tags = var.tags

  depends_on = [azurerm_resource_group.rg]
}

# Data source to find the managed resource group containing the access connector
data "azurerm_resources" "databricks_managed_rg" {
  name                = "unity-catalog-access-connector"
  type                = "Microsoft.Databricks/accessConnectors"
  
  depends_on = [azurerm_databricks_workspace.workspace]
}

# Data source for existing Databricks Access Connector created by workspace
data "azurerm_databricks_access_connector" "access_connector" {
  name                = "unity-catalog-access-connector"
  resource_group_name = data.azurerm_resources.databricks_managed_rg.resources[0].resource_group_name

  depends_on = [data.azurerm_resources.databricks_managed_rg]
}

# Role Assignment: Storage Blob Data Contributor for Access Connector's Managed Identity
resource "azurerm_role_assignment" "storage_role" {
  scope              = azurerm_storage_account.metastore.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id       = data.azurerm_databricks_access_connector.access_connector.identity[0].principal_id

  depends_on = [data.azurerm_databricks_access_connector.access_connector]
}


# Get object id for service principal used by Terraform
data "azurerm_client_config" "current" {}


# Key Vault for storing secrets 
resource "azurerm_key_vault" "kv" {
  name                = "akv-dbx"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = var.tenant_id
  sku_name            = "standard"

  purge_protection_enabled = false
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = var.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
      "List",
      "Create",
      "Delete"
    ]

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete"
    ]
  }

  access_policy {
    tenant_id = var.tenant_id
    object_id = var.az_admin_user_object_id

    key_permissions = [
      "Get",
      "List",
      "Create",
      "Delete"
    ]

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete"
    ]
  }
}


# Storage Account for raw data
resource "azurerm_storage_account" "raw_data" {
  name                     = "rawdatastorage123456"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  https_traffic_only_enabled = true
  is_hns_enabled           = true

  tags = var.tags

  depends_on = [azurerm_resource_group.rg]
}



