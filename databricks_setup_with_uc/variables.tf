variable "tenant_id" {
  type    = string
  default = "XXXX"
}

variable "subscriber_id" {
  type    = string
  default = "XXXX"
}

variable "client_id" {
  type    = string
  default = "XXXX"
}

variable "client_secret" {
  type    = string
  default = "XXXX"
}

variable "location" {
  type        = string
  description = "Azure region where resources will be created"
  default     = "East US"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
  default     = "rg-databricks"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "dev"
}

variable "storage_account_name" {
  type        = string
  description = "Name of the storage account (must be globally unique, lowercase, 3-24 characters)"
  default     = "kaniniprostorageaccountdev"
}

variable "storage_container_name" {
  type        = string
  description = "Name of the storage container"
  default     = "databricks-container"
}

variable "access_connector_name" {
  type        = string
  description = "Name of the Databricks access connector"
  default     = "databricks-connector"
}

variable "workspace_name" {
  type        = string
  description = "Name of the Databricks workspace"
  default     = "databricks-workspace"
}

variable "databricks_sku" {
  type        = string
  description = "SKU of the Databricks workspace (standard, premium, or trial)"
  default     = "premium"
}

