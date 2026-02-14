from __future__ import annotations

import os
import time
import uuid
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .registry import build_registry
from .stats import MarketStats


app = FastAPI(title="AI Marketplace (Local)", version="0.1")

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())
stats = MarketStats(out_path=os.path.join(WORKSPACE, "memory", "market-stats.jsonl"))
agents = build_registry()


class InvokeReq(BaseModel):
    user_id: str = "local"
    prompt: str


@app.get("/", response_class=HTMLResponse)
def home():
    rows = []
    for a in agents.values():
        rows.append(f"<tr><td>{a.agent_id}</td><td>{a.version}</td><td>{a.price_per_use}</td></tr>")

    html = f"""
    <html>
      <head><title>AI Marketplace (Local)</title></head>
      <body style='font-family: ui-sans-serif, system-ui; background:#050814; color:#f8f9ff;'>
        <h1 style='color:#4169e1;'>Seventh River Marketplace</h1>
        <p style='color:#a0a7c0;'>Local-only. No external calls. Vow: I didn't pull from any database.</p>

        <h2 style='color:#e6e6fa;'>Agents</h2>
        <table border='0' cellpadding='6' cellspacing='0'>
          <tr style='color:#28f0ff;'><th align='left'>agent_id</th><th align='left'>version</th><th align='left'>price</th></tr>
          {''.join(rows)}
        </table>

        <h2 style='color:#e6e6fa;'>Invoke</h2>
        <form method='post' action='/invoke/echo'>
          <label>Prompt</label><br/>
          <textarea name='prompt' rows='4' cols='60'></textarea><br/>
          <button type='submit' style='background:#4169e1;color:#050814;padding:8px 12px;border:0;'>Fire</button>
        </form>

        <h2 style='color:#e6e6fa;'>Revenue</h2>
        <pre style='color:#a0a7c0;'>{stats.app_revenue}</pre>
      </body>
    </html>
    """
    return HTMLResponse(html)


@app.post("/invoke/{agent_id}")
def invoke(agent_id: str, req: InvokeReq):
    if agent_id not in agents:
        return {"ok": False, "error": "unknown agent"}

    agent = agents[agent_id]
    run_id = str(uuid.uuid4())

    t0 = time.time()
    try:
        resp = agent.safe_run(req.prompt)
        ledger = stats.record_task(req.user_id, agent.agent_id, agent.price_per_use, task_id=run_id, kind="invoke")
        return {
            "ok": True,
            "run_id": run_id,
            "agent_id": agent.agent_id,
            "version": agent.version,
            "latency_s": time.time() - t0,
            "result": resp.text,
            "ledger": ledger,
        }
    except Exception as e:
        return {"ok": False, "run_id": run_id, "error": f"Error: {e}"}
