<#
Apply Seventh River palette to OpenClaw's bundled TUI JS.

Why:
- `openclaw tui` currently ships with a hardcoded palette inside `dist/tui-*.js`.
- Global npm updates may overwrite those files.

This script re-applies the exact palette swap safely (idempotent).

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\apply-seventh-river-theme.ps1

Optional env override:
  $env:OPENCLAW_DIST = "C:\\Users\\<you>\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist"
#>

$ErrorActionPreference = 'Stop'

function Get-OpenClawDistPath {
  if ($env:OPENCLAW_DIST -and (Test-Path $env:OPENCLAW_DIST)) {
    return (Resolve-Path $env:OPENCLAW_DIST).Path
  }

  # Default global npm path on Windows
  $default = Join-Path $env:APPDATA 'npm\node_modules\openclaw\dist'
  if (Test-Path $default) {
    return (Resolve-Path $default).Path
  }

  throw "Could not find OpenClaw dist directory. Set OPENCLAW_DIST env var to the correct path."
}

$dist = Get-OpenClawDistPath
Write-Host "OpenClaw dist: $dist"

$targets = @(
  (Join-Path $dist 'tui-B0PFk5gW.js'),
  (Join-Path $dist 'tui-Dp_597lz.js')
)

# Original palette block (must match exact upstream text).
$old = @'
const palette = {
	text: "#E8E3D5",
	dim: "#7B7F87",
	accent: "#F6C453",
	accentSoft: "#F2A65A",
	border: "#3C414B",
	userBg: "#2B2F36",
	userText: "#F3EEE0",
	systemText: "#9BA3B2",
	toolPendingBg: "#1F2A2F",
	toolSuccessBg: "#1E2D23",
	toolErrorBg: "#2F1F1F",
	toolTitle: "#F6C453",
	toolOutput: "#E1DACB",
	quote: "#8CC8FF",
	quoteBorder: "#3B4D6B",
	code: "#F0C987",
	codeBlock: "#1E232A",
	codeBorder: "#343A45",
	link: "#7DD3A5",
	error: "#F97066",
	success: "#7DD3A5"
};
'@

# Seventh River palette block.
$new = @'
const palette = {
	// Seventh River (Prana) — borderless, river-light focus
	text: "#F8F9FF",      // ink
	dim: "#A0A7C0",       // whisper
	accent: "#4169E1",    // river
	accentSoft: "#E6E6FA",// breath
	border: "#050814",    // core (invisible border)
	userBg: "#050814",    // core
	userText: "#F8F9FF",  // ink
	systemText: "#A0A7C0", // whisper
	toolPendingBg: "#050814",
	toolSuccessBg: "#050814",
	toolErrorBg: "#050814",
	toolTitle: "#4169E1", // river
	toolOutput: "#F8F9FF",
	quote: "#28F0FF",     // axon
	quoteBorder: "#050814",
	code: "#E6E6FA",      // breath
	codeBlock: "#050814",
	codeBorder: "#050814",
	link: "#28F0FF",      // axon
	error: "#FF5370",     // danger
	success: "#1DE9B6"    // success
};
'@

foreach ($file in $targets) {
  if (-not (Test-Path $file)) {
    Write-Warning "Missing: $file (skipping)"
    continue
  }

  $txt = Get-Content -Raw -Path $file -Encoding UTF8

  if ($txt -match 'Seventh River \(Prana\)') {
    Write-Host "Already patched: $file"
    continue
  }

  if ($txt -notlike "*$old*") {
    throw "Upstream palette block not found in $file. OpenClaw may have changed; update the script."
  }

  $patched = $txt.Replace($old, $new)
  Set-Content -Path $file -Value $patched -Encoding UTF8
  Write-Host "Patched: $file"
}

Write-Host "Seventh River theme applied."