#Requires -Version 5.1
$ErrorActionPreference = "SilentlyContinue"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$syncScript = Join-Path $projectRoot "scripts\git-sync.ps1"

if (-not (Test-Path $syncScript)) {
    exit 0
}

$previousPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$output = & powershell -ExecutionPolicy Bypass -File $syncScript -Quiet 2>&1
$exitCode = $LASTEXITCODE
$ErrorActionPreference = $previousPreference

if ($exitCode -ne 0) {
    $msg = ($output | Out-String).Trim()
    if ($msg.Length -gt 500) { $msg = $msg.Substring(0, 500) + "..." }
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    @{
        followup_message = "Git auto-sync nije uspio. Pokreni @git-sync agenta ili scripts/git-sync.ps1 ručno. Detalj: $msg"
    } | ConvertTo-Json -Compress
}

exit 0
