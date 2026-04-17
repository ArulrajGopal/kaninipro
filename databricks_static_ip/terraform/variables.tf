#azure credentials
variable "tenant_id" {
  type        = string
  description = "Azure AD Tenant ID"
  default     = "XXXX"
}

variable "subscription_id" {
  type        = string
  description = "Azure Subscription ID"
  default     = "XXXX"
}

variable "client_id" {
  type        = string
  description = "Azure Service Principal Client ID"
  default     = "XXXX"
}

variable "client_secret" {
  type        = string
  description = "Azure Service Principal Client Secret"
  sensitive   = true
  default     = "XXXX"
}

variable "account_id" {
  type        = string
  description = "Azure Databricks Account ID"
  sensitive   = true
  default     = "XXXX"
}

variable "sql_admin_username" {
  description = "Administrator username for SQL Server"
  type        = string
  default     = "XXXX"
}

variable "sql_admin_password" {
  description = "Administrator password for SQL Server"
  type        = string
  sensitive   = true
  default     = "XXXX"
}


#resource group
variable "databricks_resource_group_name" {
  type        = string
  description = "Name of the Azure Resource Group"
  default     = "rg-databricks-metastore"
}

variable "adls_resource_group_name" {
  type        = string
  description = "Name of the Azure Resource Group"
  default     = "rg-adls"
}

variable "network_resource_group_name" {
  type        = string
  description = "Name of the Azure Resource Group"
  default     = "rg-databricks-network"
}

variable "sql_server_rg" {
  type        = string
  description = "Name of the Azure Resource Group"
  default     = "rg-sql-server"
}


#other variables
variable "location" {
  type        = string
  description = "Azure region for resources"
  default     = "South India"
}

variable "storage_account_name" {
  type        = string
  description = "Name of the storage account for metastore (must be globally unique and lowercase)"
  default     = "dbmetastore123456"
}

variable "metastore_container_name" {
  type        = string
  description = "Name of the container in the storage account"
  default     = "metastore"
}

variable "workspace_name" {
  type        = string
  description = "Name of the Databricks workspace"
  default     = "databricks_workspace"
}

variable "databricks_sku" {
  type        = string
  description = "The SKU of the Databricks workspace (standard, premium, or trial)"
  default     = "premium"
}

variable "tags" {
  type        = map(string)
  description = "Tags to be applied to all resources"
  default = {
    Environment = "Production"
    ManagedBy   = "Terraform"
    Application = "Databricks"
  }
}


variable "sql_server_name" {
  description = "Name of the Azure SQL Server (must be globally unique)"
  type        = string
  default     = "kaninipro-server"
}

variable "sql_database_name" {
  description = "Name of the Azure SQL Database"
  type        = string
  default     = "kaninipro_db"
}

