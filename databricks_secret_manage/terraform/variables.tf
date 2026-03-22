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

variable "az_admin_user_object_id" {
  type        = string
  description = "The object ID of the Azure AD user to be assigned as Databricks admin"
  default     = "your_admin_object_id"
}



