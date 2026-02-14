<#
Builds dist/full_ai_marketplace_ready.zip from the current OpenClaw workspace.

Includes:
- ABOUT.md, SEVENTH_RIVER.md
- fire/
- scripts/
- themes/
- memory/2026-02-14.md and memory/2026-02-14.summary.json (if present)

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\build-full-ai-marketplace-zip.ps1
#>

$ErrorActionPreference = 'Stop'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$dist = Join-Path $root 'dist'
$zipPath = Join-Path $dist 'full_ai_marketplace_ready.zip'

New-Item -ItemType Directory -Force -Path $dist | Out-Null
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

$include = @(
  'ABOUT.md',
  'SEVENTH_RIVER.md',
  'fire',
  'scripts',
  'themes',
  'memory\2026-02-14.md',
  'memory\2026-02-14.summary.json'
)

$paths = @()
foreach ($rel in $include) {
  $p = Join-Path $root $rel
  if (Test-Path $p) { $paths += $p }
}

if ($paths.Count -eq 0) {
  throw "Nothing to zip. Expected files not found."
}

Compress-Archive -Path $paths -DestinationPath $zipPath -Force

Write-Host "[SUCCESS] full_ai_marketplace_ready.zip created!"
Write-Host "Path: $zipPath"
