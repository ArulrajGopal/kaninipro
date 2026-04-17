resource "azurerm_resource_group" "rgntwrk" {
  name     = var.network_resource_group_name
  location = var.location
  tags     = var.tags
}


resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-databricks"
  address_space       = ["10.10.0.0/16"]
  location            = azurerm_resource_group.rgntwrk.location
  resource_group_name = azurerm_resource_group.rgntwrk.name
}

resource "azurerm_subnet" "public" {
  name                 = "public-subnet"
  resource_group_name  = azurerm_resource_group.rgntwrk.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.10.1.0/24"]

  delegation {
    name = "databricks-delegation"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
}

resource "azurerm_subnet" "private" {
  name                 = "private-subnet"
  resource_group_name  = azurerm_resource_group.rgntwrk.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.10.2.0/24"]

  delegation {
    name = "databricks-delegation"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
}

resource "azurerm_public_ip" "nat_ip" {
  name                = "databricks-nat-ip"
  location            = azurerm_resource_group.rgntwrk.location
  resource_group_name = azurerm_resource_group.rgntwrk.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_nat_gateway" "nat" {
  name                = "databricks-nat"
  location            = azurerm_resource_group.rgntwrk.location
  resource_group_name = azurerm_resource_group.rgntwrk.name
  sku_name            = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "nat_ip_assoc" {
  nat_gateway_id       = azurerm_nat_gateway.nat.id
  public_ip_address_id = azurerm_public_ip.nat_ip.id
}


resource "azurerm_subnet_nat_gateway_association" "public_assoc" {
  subnet_id      = azurerm_subnet.public.id
  nat_gateway_id = azurerm_nat_gateway.nat.id
}

resource "azurerm_subnet_nat_gateway_association" "private_assoc" {
  subnet_id      = azurerm_subnet.private.id
  nat_gateway_id = azurerm_nat_gateway.nat.id
}


resource "azurerm_network_security_group" "public_nsg" {
  name                = "public-subnet-nsg"
  location            = azurerm_resource_group.rgntwrk.location
  resource_group_name = azurerm_resource_group.rgntwrk.name
}

resource "azurerm_network_security_group" "private_nsg" {
  name                = "private-subnet-nsg"
  location            = azurerm_resource_group.rgntwrk.location
  resource_group_name = azurerm_resource_group.rgntwrk.name
}

resource "azurerm_subnet_network_security_group_association" "public_assoc" {
  subnet_id                 = azurerm_subnet.public.id
  network_security_group_id = azurerm_network_security_group.public_nsg.id
}

resource "azurerm_subnet_network_security_group_association" "private_assoc" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private_nsg.id
}