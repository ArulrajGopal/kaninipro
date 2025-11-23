## configure

      databricks configure


## confirming profiles

      databricks auth profiles


## list clusters

      databricks clusters list


## get cluster details 

      databricks clusters get <cluster_id>
      

## start the cluster

      databricks clusters start <cluster_id>
      

## stop the cluster

      databricks clusters delete <cluster_id>


## list jobs

      databricks jobs list

## list job runs

      databricks jobs list-runs

## Extract the job run from some particular timing 

      $from = [int64]((Get-Date).AddHours(-3).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds

      databricks jobs list-runs --job-id 26288366538638 --start-time-from $from


## Capture the run along with result

      databricks jobs export-run <run_id> --views-to-export ALL > run_export.json

      powershell -ExecutionPolicy Bypass -File .\convert_json_to_html.ps1 -JsonFile "run_export.json" -HtmlFile "run_log.html"
    

## check latest few job status along with run duration

      powershell -ExecutionPolicy Bypass -File .\job_status.ps1 -JobId <job_id> -Hours 5

## get users list 

      databricks users list

## get user details

      databricks users get <user_id>

      
