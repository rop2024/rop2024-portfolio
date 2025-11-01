# PowerShell wrapper to start the Tailwind watcher for the theme from repo root
# Usage: Open PowerShell in the project root and run: .\scripts\run-theme-dev.ps1

$ErrorActionPreference = 'Stop'

# Resolve project root (assumes this script lives in <project>/scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$projectRoot = Split-Path -Parent $scriptDir

Write-Host "Project root: $projectRoot"

# Path to theme static_src
$themeSrc = Join-Path $projectRoot 'theme\static_src'

Set-Location $themeSrc

if (!(Test-Path node_modules)) {
    Write-Host 'node_modules not found — running npm install (this may take a moment)...'
    npm install
} else {
    Write-Host 'node_modules found — skipping install.'
}

Write-Host 'Starting Tailwind watcher (npm run dev)...'
npm run dev
