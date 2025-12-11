# Azure Databricks Workspace with Unity Catalog and Metastore

This Terraform configuration creates a complete Azure Databricks infrastructure with:
- Databricks workspace with Unity Catalog enabled
- Storage account for metastore
- User-assigned managed identity for secure access
- Role-based access control (RBAC) for storage access
- Databricks metastore with Unity Catalog and default schema

## Prerequisites

1. **Azure Subscription**: An active Azure subscription
2. **Service Principal**: An Azure AD service principal with appropriate permissions:
   - Contributor or Owner role on the subscription
3. **Terraform**: Version 1.0 or higher
4. **Azure CLI**: For authentication (optional)

## Files Structure

```
├── main.tf                 # Main infrastructure resources
├── variables.tf            # Variable definitions
├── outputs.tf              # Output values
├── terraform.tfvars        # Variable values (create and configure)
└── README.md               # This file
```

## Configuration Steps

### 1. Update Variables

Edit `terraform.tfvars` with your Azure credentials and preferences:

```hcl
tenant_id       = "your-tenant-id"
subscription_id = "your-subscription-id"
client_id       = "your-service-principal-client-id"
client_secret   = "your-service-principal-client-secret"

# Update storage account name (must be globally unique, lowercase, 3-24 chars)
storage_account_name = "dbmetastore123456"

# Other customizations as needed
resource_group_name = "rg-databricks-metastore"
location            = "East US"
```

**Note**: The `storage_account_name` must be globally unique across Azure and contain only lowercase letters and numbers.

### 2. Initialize Terraform

```bash
terraform init
```

This downloads the required providers (azurerm and databricks).

### 3. Plan the Deployment

```bash
terraform plan -out=tfplan
```

Review the resources that will be created.

### 4. Apply the Configuration

```bash
terraform apply tfplan
```

This creates all the resources. The process may take 10-15 minutes.

## Architecture Overview

### Resource Components

1. **Resource Group**: Container for all resources
2. **Storage Account**: Stores metastore data
   - Container: `metastore`
   - Access: Only via managed identity
3. **User-Assigned Managed Identity**: Secure authentication for Databricks
   - Role Assignment: `Storage Blob Data Contributor` on storage account
4. **Databricks Access Connector**: Integrates managed identity with Databricks
5. **Databricks Workspace**: Premium SKU with Unity Catalog enabled
6. **Metastore**: Unified data catalog backend storage
7. **Unity Catalog**: Data governance layer with:
   - Catalog: `main_catalog`
   - Schema: `default_schema`

## Security Features

- **Managed Identity**: No exposed credentials; uses Azure AD authentication
- **RBAC**: Fine-grained role-based access control
- **HTTPS Only**: Storage account enforces encrypted communication
- **Private Container**: Metastore storage is private, accessible only to authorized identities

## Outputs

After successful deployment, Terraform outputs:

```
databricks_workspace_url         - URL to access Databricks workspace
databricks_workspace_id          - Workspace ID
metastore_id                     - Metastore ID
metastore_storage_path           - Storage path for metastore
storage_account_name             - Storage account name
managed_identity_id              - Managed identity resource ID
unity_catalog_name               - Unity Catalog name
resource_group_name              - Resource group name
```

View outputs with:
```bash
terraform output
```

## Accessing Databricks

1. Go to the URL provided in `databricks_workspace_url` output
2. Sign in with your Azure credentials
3. You'll have access to the workspace with Unity Catalog enabled
4. Navigate to **Catalog** to see your `main_catalog` and `default_schema`

## Managing Resources

### View Current State
```bash
terraform show
```

### Update Configuration
Edit variables in `terraform.tfvars` and run:
```bash
terraform plan
terraform apply
```

### Destroy All Resources
```bash
terraform destroy
```

## Troubleshooting

### Storage Account Name Already Exists
Change `storage_account_name` in `terraform.tfvars` to a unique name.

### Authentication Failures
- Verify service principal credentials in `terraform.tfvars`
- Ensure service principal has sufficient permissions
- Check that tenant_id and subscription_id are correct

### Metastore Creation Fails
- Ensure storage account is fully created and accessible
- Verify managed identity has the correct role assignment
- Check Azure region availability for Databricks

### Access Denied to Storage
- The role assignment `Storage Blob Data Contributor` is required
- It may take a few minutes for role assignments to propagate
- Verify the managed identity principal_id in the role assignment

## Provider Information

- **AzureRM Provider**: Manages Azure resources
- **Databricks Provider**: Manages Databricks workspace, metastore, and catalog

## Cost Considerations

### Monthly Estimated Costs:
- **Databricks Workspace (Premium)**: $0.55/DBU + compute costs
- **Storage Account**: ~$20-50 (depending on usage)
- **Managed Identity**: Free
- **Total**: Varies with Databricks compute usage

See [Databricks Pricing](https://databricks.com/product/pricing) for details.

## Next Steps

1. Create clusters in the workspace
2. Create additional schemas and tables
3. Set up data ingestion pipelines
4. Configure access controls in Unity Catalog
5. Monitor usage and optimize costs

## Support

For issues or questions:
- Check Terraform documentation: https://registry.terraform.io/providers/hashicorp/azurerm
- Databricks Terraform provider: https://registry.terraform.io/providers/databricks/databricks
