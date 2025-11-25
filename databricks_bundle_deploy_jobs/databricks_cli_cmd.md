# auth login

    databricks auth login --host <databricks_url>

    databricks auth profiles

# databricks create scope

    databricks secrets create-scope myscope 

    databricks secrets list-scopes

    databricks secrets put-secret myscope adls_key --string-value <your_access_key>

# databricks bundle initialize & validate

    databricks bundle init
    
    databricks bundle validate


# databricks bundle deploy

    databricks bundle deploy

    databricks bundle deploy --profile <profile_name> --target <env_target>


# databricks bundle destory

    databricks bundle destroy

    databricks bundle destroy --profile <profile_name> --target <env_target>

