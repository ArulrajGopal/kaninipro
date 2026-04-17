# Resource Group
resource "azurerm_resource_group" "rgsql" {
  name     = var.sql_server_rg
  location = var.location
  tags     = var.tags
}


resource "azurerm_mssql_server" "sql_server" {
  name                         = var.sql_server_name
  resource_group_name          = azurerm_resource_group.rgsql.name
  location                     = azurerm_resource_group.rgsql.location
  version                      = "12.0"

  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  minimum_tls_version          = "1.2"

  tags = var.tags

  depends_on = [azurerm_resource_group.rgsql]
}

resource "azurerm_mssql_database" "sql_db" {
  name           = var.sql_database_name
  server_id      = azurerm_mssql_server.sql_server.id

  sku_name       = "Basic"   # This gives 5 DTU automatically
  max_size_gb    = 2         # Basic tier supports up to 2GB

  zone_redundant = false

  tags = var.tags

  depends_on = [azurerm_mssql_server.sql_server]
}
