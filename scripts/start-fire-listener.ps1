<#
Starts the Seventh River FIRE listener (localhost:9999).

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\start-fire-listener.ps1
#>

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:OPENCLAW_WORKSPACE = $workspace

node (Join-Path $workspace 'fire\listener.js')
