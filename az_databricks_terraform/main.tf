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
  subscription_id = var.subscriber_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

provider "databricks" {
  host                = azurerm_databricks_workspace.workspace.workspace_url
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

# User Assigned Managed Identity for Databricks
resource "azurerm_user_assigned_identity" "databricks_identity" {
  name                = var.managed_identity_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  tags = var.tags

  depends_on = [azurerm_resource_group.rg]
}

# Role Assignment: Storage Blob Data Contributor for Managed Identity
resource "azurerm_role_assignment" "storage_role" {
  scope              = azurerm_storage_account.metastore.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id       = azurerm_user_assigned_identity.databricks_identity.principal_id

  depends_on = [azurerm_user_assigned_identity.databricks_identity]
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


# Databricks Access Connector for Managed Identity Integration
resource "azurerm_databricks_access_connector" "access_connector" {
  name                = var.access_connector_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.databricks_identity.id
    ]
  }

  tags = var.tags

  depends_on = [azurerm_user_assigned_identity.databricks_identity]
}

# Databricks Admin Users
resource "databricks_user" "admin_users" {
  for_each = toset(var.admin_user_email)

  user_name = each.value

  depends_on = [azurerm_databricks_workspace.workspace]
}

# Databricks Regular Users
resource "databricks_user" "regular_users" {
  for_each = toset(var.user_email)

  user_name = each.value

  depends_on = [azurerm_databricks_workspace.workspace]
}

# Databricks Admin Group
resource "databricks_group" "admin_group" {
  display_name = "Admins"
  
  depends_on = [azurerm_databricks_workspace.workspace]
}

# Databricks User Group
resource "databricks_group" "user_group" {
  display_name = "Users"
  
  depends_on = [azurerm_databricks_workspace.workspace]
}

# Add admin users to admin group
resource "databricks_group_member" "admin_members" {
  for_each = toset(var.admin_user_email)

  group_id  = databricks_group.admin_group.id
  member_id = databricks_user.admin_users[each.value].id

  depends_on = [databricks_user.admin_users, databricks_group.admin_group]
}

# Add regular users to user group
resource "databricks_group_member" "user_members" {
  for_each = toset(var.user_email)

  group_id  = databricks_group.user_group.id
  member_id = databricks_user.regular_users[each.value].id

  depends_on = [databricks_user.regular_users, databricks_group.user_group]
}

