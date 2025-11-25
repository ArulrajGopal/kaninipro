
databricks auth login --host https://adb-399753609440280.0.azuredatabricks.net

databricks auth login --host https://adb-1120177612362729.9.azuredatabricks.net

databricks auth login --host https://adb-3030692488866941.1.azuredatabricks.net


databricks auth profiles




    databricks secrets create-scope myscope

    databricks secrets list-scopes

    databricks secrets put-secret myscope adls_key --string-value <your_access_key>

    databricks bundle init
    
    databricks bundle validate





databricks bundle deploy

databricks bundle deploy --profile profile2 --target test

databricks bundle deploy --profile profile3 --target prod


databricks bundle destroy

databricks bundle destroy --profile profile2 --target test

databricks bundle destroy --profile profile3 --target prod
