param(
    [Parameter(Mandatory = $true)]
    [string]$JsonFile,

    [Parameter(Mandatory = $true)]
    [string]$HtmlFile
)

# ---------------------------------------------
# Convert Databricks run export JSON → HTML
# ---------------------------------------------

# Load JSON
$run = Get-Content -Path $JsonFile -Raw | ConvertFrom-Json

# Extract HTML and save
$run.views[0].content | Out-File -FilePath $HtmlFile -Encoding utf8

# Open the HTML file
Start-Process $HtmlFile

