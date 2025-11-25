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

resource "azurerm_storage_account" "storage_account_test" {
  name                     = "kaniniproadlstest"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = "Terraform"
  }
}

resource "azurerm_storage_account" "storage_account_prod" {
  name                     = "kaniniproadlsprod"
  resource_group_name       = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  tags = {
    environment = "Terraform"
  }
}

# storage containers

resource "azurerm_storage_container" "container_source_dev" {
  name                  = "source"
  storage_account_id    = azurerm_storage_account.storage_account_dev.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "container_target_dev" {
  name                  = "target"
  storage_account_id    = azurerm_storage_account.storage_account_dev.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "container_source_test" {
  name                  = "source"
  storage_account_id    = azurerm_storage_account.storage_account_test.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "container_target_test" {
  name                  = "target"
  storage_account_id    = azurerm_storage_account.storage_account_test.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "container_source_prod" {
  name                  = "source"
  storage_account_id    = azurerm_storage_account.storage_account_prod.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "container_target_prod" {
  name                  = "target"
  storage_account_id    = azurerm_storage_account.storage_account_prod.id
  container_access_type = "private"
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




resource "azurerm_resource_group" "rg_test" {
  name     = "dbx-test"
  location = "South India"
}


resource "azurerm_databricks_workspace" "dbx2" {
  name                = "kaninipro-dbx1-test"
  resource_group_name = azurerm_resource_group.rg_test.name
  location            = azurerm_resource_group.rg_test.location
  sku                 = "premium"

    tags = {
    environment = "Terraform"
  }

  depends_on = [azurerm_databricks_workspace.dbx1]
}




resource "azurerm_resource_group" "rg_prod" {
  name     = "dbx-prod"
  location = "South India"
}


resource "azurerm_databricks_workspace" "dbx3" {
  name                = "kaninipro-dbx1-prod"
  resource_group_name = azurerm_resource_group.rg_prod.name
  location            = azurerm_resource_group.rg_prod.location
  sku                 = "premium"

    tags = {
    environment = "Terraform"
  }

  depends_on = [azurerm_databricks_workspace.dbx2]
}


