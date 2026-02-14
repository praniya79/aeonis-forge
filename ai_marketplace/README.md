# AI Marketplace (local)

A tiny local-only web app that demonstrates:
- agent registry
- invoke endpoint
- verifier (prohibited words)
- market stats ledger (JSONL in `memory/market-stats.jsonl`)

## Run

```powershell
pip install -r ai_marketplace\requirements.txt
powershell -ExecutionPolicy Bypass -File .\scripts\start-ai-marketplace.ps1
```

Then open:
- http://127.0.0.1:9997

## Notes
- Local-only bind (127.0.0.1)
- No external network calls
