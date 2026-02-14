<#
One-click setup + run for the local AI Marketplace.
- installs python deps
- starts uvicorn server on 127.0.0.1:9997

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup-ai-marketplace.ps1
#>

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $workspace

Write-Host "Installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r .\ai_marketplace\requirements.txt

Write-Host "Starting AI Marketplace on http://127.0.0.1:9997 ..."
$env:OPENCLAW_WORKSPACE = $workspace
python -m uvicorn ai_marketplace.app:app --host 127.0.0.1 --port 9997
