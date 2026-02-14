<#
Removes Seventh River FIRE listener autostart task.

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\uninstall-fire-autostart.ps1
#>

$ErrorActionPreference = 'Stop'

$taskName = 'SeventhRiver-FIRE'

schtasks /Delete /F /TN $taskName | Out-Host
Write-Host "Removed task: $taskName"