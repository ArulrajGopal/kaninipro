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

## find the utc time 2 hours from now (powershell script)

      [int64]((Get-Date).AddHours(-2).ToUniversalTime() - [datetime]'1970-01-01').TotalMilliseconds

## run the job runs only after this time

      databricks jobs list-runs --job-id <job_run_id> --start-time-from <utc_time>





      
