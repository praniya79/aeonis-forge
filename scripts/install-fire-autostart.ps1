<#
Installs Seventh River FIRE listener autostart (Windows Task Scheduler).

Creates a per-user task that runs at logon:
- starts node fire/listener.js via scripts/start-fire-listener.ps1

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\install-fire-autostart.ps1

Remove:
  powershell -ExecutionPolicy Bypass -File .\scripts\uninstall-fire-autostart.ps1
#>

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$startScript = Join-Path $workspace 'scripts\start-fire-listener.ps1'

if (-not (Test-Path $startScript)) {
  throw "Missing $startScript"
}

$taskName = 'SeventhRiver-FIRE'

# Quote carefully for schtasks
$tr = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$startScript`""

# Create / replace
schtasks /Create /F /SC ONLOGON /RL LIMITED /TN $taskName /TR $tr | Out-Host

Write-Host "Installed Task Scheduler task: $taskName"
Write-Host "It will start the FIRE listener at logon."
Write-Host "To test now: schtasks /Run /TN $taskName"
