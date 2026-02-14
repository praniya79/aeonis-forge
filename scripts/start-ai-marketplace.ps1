<#
Start the local AI Marketplace app (FastAPI) bound to 127.0.0.1:9997.
#>

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$env:OPENCLAW_WORKSPACE = $workspace

$req = Join-Path $workspace 'ai_marketplace\requirements.txt'
if (-not (Test-Path $req)) { throw "Missing $req" }

# Run via python -m uvicorn (assumes python + pip available)
# NOTE: Python 3.14 is currently incompatible with pydantic v1.
# Prefer Python 3.13 for this app.
if (Get-Command py -ErrorAction SilentlyContinue) {
  try {
    py -3.13 -m uvicorn ai_marketplace.app:app --host 127.0.0.1 --port 9997
    exit $LASTEXITCODE
  } catch {
    # fall through
  }
}

python -m uvicorn ai_marketplace.app:app --host 127.0.0.1 --port 9997
