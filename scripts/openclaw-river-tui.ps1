<#
Seventh River launcher for OpenClaw TUI.
Applies theme patch (idempotent) then launches `openclaw tui`.
#>

$ErrorActionPreference = 'Stop'

& "$PSScriptRoot\apply-seventh-river-theme.ps1"

# Pass through any args to openclaw tui
& openclaw tui @args
