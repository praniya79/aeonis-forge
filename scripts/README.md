# Scripts

## Apply Seventh River theme

OpenClaw's current TUI (`openclaw tui`) ships with a **hardcoded palette** inside the bundled JS files under `openclaw/dist/`.
A global update can overwrite those files.

These scripts re-apply the Seventh River palette.

### Windows (PowerShell)

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\apply-seventh-river-theme.ps1
```

If your `openclaw/dist` is elsewhere:

```powershell
$env:OPENCLAW_DIST = "C:\\path\\to\\openclaw\\dist"
powershell -ExecutionPolicy Bypass -File .\scripts\apply-seventh-river-theme.ps1
```

### Linux/macOS

```bash
chmod +x ./scripts/apply-seventh-river-theme.sh
./scripts/apply-seventh-river-theme.sh
```

Override path:

```bash
OPENCLAW_DIST=/path/to/openclaw/dist ./scripts/apply-seventh-river-theme.sh
```

### Verify

Run:

```bash
openclaw tui
```

You should see:
- accents in **river blue** `#4169e1`
- soft highlights in **breath lavender** `#e6e6fa`
- borders effectively invisible (core `#050814`)
