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

### find the utc time 2 hours from now (powershell script)

      [int64]((Get-Date).AddHours(-2).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds

### run the job runs only after this time

      databricks jobs list-runs --job-id <job_run_id> --start-time-from <utc_time>


## Capture the run along with result

      databricks jobs export-run <run_id> --views-to-export ALL > run_export.json

### script to convert the json into html which can be lodaed into databricks or viewed with browser itself.

      $run = Get-Content run_export.json -Raw | ConvertFrom-Json
      $run.views[0].content | Out-File -FilePath .\run_log.html -Encoding utf8
      Start-Process .\run_log.html

## check latest few job status along with run duration

      powershell -ExecutionPolicy Bypass -File .\job_status.ps1 -JobId <job_id> -Hours 5

## get users list 

      databricks users list

## get user details

      databricks users get <user_id>

      
