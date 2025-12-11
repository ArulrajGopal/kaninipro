variable "tenant_id" {
  type        = string
  description = "Azure AD Tenant ID"
  default     = "XXXX"
}

variable "subscriber_id" {
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

variable "resource_group_name" {
  type        = string
  description = "Name of the Azure Resource Group"
  default     = "rg-databricks-metastore"
}

variable "location" {
  type        = string
  description = "Azure region for resources"
  default     = "East US"
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

variable "managed_identity_name" {
  type        = string
  description = "Name of the user-assigned managed identity"
  default     = "databricks-identity"
}

variable "workspace_name" {
  type        = string
  description = "Name of the Databricks workspace"
  default     = "databricks-workspace"
}

variable "databricks_sku" {
  type        = string
  description = "Databricks workspace SKU (Premium or Standard)"
  default     = "premium"
}

variable "metastore_name" {
  type        = string
  description = "Name of the Databricks metastore"
  default     = "primary-metastore"
}

variable "storage_credential_name" {
  type        = string
  description = "Name of the Databricks storage credential"
  default     = "metastore-credential"
}

variable "access_connector_name" {
  type        = string
  description = "Name of the Databricks access connector"
  default     = "databricks-access-connector"
}

variable "unity_catalog_name" {
  type        = string
  description = "Name of the Unity Catalog"
  default     = "main_catalog"
}

variable "schema_name" {
  type        = string
  description = "Name of the default schema in Unity Catalog"
  default     = "default_schema"
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