# auth login

    databricks auth login --host <databricks_url>

    databricks auth profiles

# databricks create scope

    databricks secrets create-scope myscope 

    databricks secrets list-scopes

    databricks secrets put-secret myscope adls_key --string-value <your_access_key>

# databricks bundle initialize

    databricks bundle init
    
    databricks bundle validate





databricks bundle deploy

databricks bundle deploy --profile profile2 --target test

databricks bundle deploy --profile profile3 --target prod


databricks bundle destroy

databricks bundle destroy --profile profile2 --target test

databricks bundle destroy --profile profile3 --target prod
