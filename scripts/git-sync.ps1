#Requires -Version 5.1
param(
    [switch]$Quiet,
    [switch]$SetupRemote,
    [string]$RemoteUrl = "",
    [string]$CommitMessage = ""
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

function Write-Info([string]$Message) {
    if (-not $Quiet) { Write-Host $Message }
}

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)

    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & git @GitArgs 2>&1 | Out-Null
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $previousPreference

    if ($exitCode -ne 0) {
        throw "git $($GitArgs -join ' ') nije uspio (exit $exitCode)."
    }
}

function Get-RemoteUrl {
    try {
        return (git remote get-url origin 2>$null)
    } catch {
        return $null
    }
}

# Init repo if needed
if (-not (Test-Path ".git")) {
    Write-Info "Inicijaliziram git repozitorij..."
    git init | Out-Null
    git branch -M main 2>$null
}

# First-time GitHub setup
if ($SetupRemote -or (-not (Get-RemoteUrl) -and $RemoteUrl)) {
    if ($RemoteUrl) {
        if (Get-RemoteUrl) {
            git remote set-url origin $RemoteUrl
        } else {
            git remote add origin $RemoteUrl
        }
        Write-Info "Remote postavljen: $RemoteUrl"
    } elseif (Get-Command gh -ErrorAction SilentlyContinue) {
        Write-Info "Kreiram GitHub repo preko gh CLI..."
        gh repo create diplomski-novi --private --source=. --remote=origin --description "Diplomski rad - radna verzija"
        if ($LASTEXITCODE -ne 0) { throw "gh repo create nije uspio." }
    } else {
        throw @"
Nema postavljenog remote-a. Odaberi jedno:

1. Instaliraj GitHub CLI: winget install GitHub.cli
   Zatim pokreni: .\scripts\git-sync.ps1 -SetupRemote

2. Ručno kreiraj repo na https://github.com/new (ime: diplomski-novi)
   Zatim pokreni:
   .\scripts\git-sync.ps1 -RemoteUrl "https://github.com/TVOJ_USERNAME/diplomski-novi.git"
"@
    }
}

# Stage all tracked-worthy changes
git add -A

$status = git status --porcelain
if (-not $status) {
    Write-Info "Nema promjena za commit."
    $remote = Get-RemoteUrl
    if ($remote) {
        Invoke-Git fetch origin
        Invoke-Git pull --ff-only origin main
        Invoke-Git push -u origin main
        Write-Info "Sync OK (bez novih commita)."
    }
    exit 0
}

if (-not $CommitMessage) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $CommitMessage = "Auto-sync: $timestamp"
}

git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) { throw "Commit nije uspio." }

Write-Info "Commit: $CommitMessage"

$remote = Get-RemoteUrl
if (-not $remote) {
    Write-Info "Commit lokalno spremljen. Za upload pokreni -SetupRemote ili postavi -RemoteUrl."
    exit 0
}

Invoke-Git fetch origin
Invoke-Git pull --rebase origin main
Invoke-Git push -u origin main

Write-Info "Upload na GitHub uspješan: $remote"
