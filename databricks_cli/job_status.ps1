param(
    [Parameter(Mandatory=$true)]
    [string]$JobId,

    [Parameter(Mandatory=$true)]
    [int]$Hours
)

# ---------------------------------------------
# 1. Calculate "last X hours" in epoch milliseconds (UTC)
# ---------------------------------------------
$fromDate = (Get-Date).AddHours(-$Hours)
$fromUtc  = $fromDate.ToUniversalTime()

$from = [int64](
    $fromUtc - [datetime]'1970-01-01'
).TotalMilliseconds

# ---------------------------------------------
# 2. Fetch runs from Databricks
# ---------------------------------------------
$runs = databricks jobs list-runs `
    --job-id $JobId `
    --start-time-from $from `
    --output JSON | ConvertFrom-Json

# ---------------------------------------------
# 3. Format + print output
# ---------------------------------------------
$runs | ForEach-Object {
    $duration = [TimeSpan]::FromMilliseconds($_.run_duration)
    [PSCustomObject]@{
        'Job ID'       = $_.job_id
        'Run ID'       = $_.run_id
        'Result State' = $_.state.result_state
        'Duration'     = $duration.ToString("hh\:mm\:ss")
        'URL'          = $_.run_page_url
    }
} | Format-Table -AutoSize
