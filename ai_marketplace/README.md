# AI Marketplace (local)

A tiny local-only web app that demonstrates:
- agent registry
- invoke endpoint
- verifier (prohibited words)
- market stats ledger (JSONL in `memory/market-stats.jsonl`)

## Important: Python version

You're currently on **Python 3.14**.

- **Pydantic v1 (1.10.x) is not compatible with Python 3.14** (it raises runtime config/type inference errors).
- This app therefore targets **FastAPI + Pydantic v2**, which requires `pydantic-core` wheels.

If installing `pydantic-core` fails or tries to build from source, the quickest fix is:

- Install **Python 3.12 or 3.13** and use that interpreter for the app.

## Run

```powershell
py -3.13 -m pip install -r ai_marketplace\requirements.txt
py -3.13 -m uvicorn ai_marketplace.app:app --host 127.0.0.1 --port 9997
```

Then open:
- http://127.0.0.1:9997

## Notes
- Local-only bind (127.0.0.1)
- No external network calls
