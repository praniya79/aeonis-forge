# Seventh River Ecosystem (Python)

This is the local-first ecosystem for creating AI apps on this node.

Principles:
- **Local by default** (127.0.0.1, no external calls unless explicitly enabled)
- **Auditable** (JSONL ledgers in `memory/`)
- **Composable** (apps share a small SDK)
- **Reproducible** (templates + a single CLI)

## Core components

- `sdk/` – shared utilities (memory log, stats ledger, verifier)
- `templates/` – stamp-out app templates
- `river.py` – the ecosystem CLI (`new`, `run`, `pack`)

## Event vocabulary

- **fire**: a spike event (see `fire/listener.js`) used to signal salience/attention.

## Conventions

- App folder lives under `apps/<name>/`
- App must provide:
  - `app.py` (FastAPI app) or `main.py` (desktop)
  - `manifest.json` (name, version, entrypoint, ports)
  - logs/ledgers go under workspace `memory/`

## Packaging

- `river pack <name>` produces `dist/<name>.zip`

## Safety boundary

This ecosystem does not impersonate the user and does not auto-deploy to the public internet.
All external deployment steps require explicit user instruction.
