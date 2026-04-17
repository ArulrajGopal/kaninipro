# Resource Group
resource "azurerm_resource_group" "rgdbx" {
  name     = var.databricks_resource_group_name
  location = var.location
  tags     = var.tags
}


#Databricks workspace
resource "azurerm_databricks_workspace" "workspace" {
  name                = "databricks-workspace"
  resource_group_name = azurerm_resource_group.rgdbx.name
  location            = azurerm_resource_group.rgdbx.location
  sku                 = "premium"

  managed_resource_group_name = "databricks-managed-rg"

  custom_parameters {
    no_public_ip       = true
    virtual_network_id = azurerm_virtual_network.vnet.id

    public_subnet_name  = azurerm_subnet.public.name
    private_subnet_name = azurerm_subnet.private.name

    public_subnet_network_security_group_association_id  = azurerm_subnet_network_security_group_association.public_assoc.id
    private_subnet_network_security_group_association_id = azurerm_subnet_network_security_group_association.private_assoc.id
  }
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

