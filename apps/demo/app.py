import os
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="demo", version="0.1")

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())


class InvokeReq(BaseModel):
    user_id: str = "local"
    prompt: str


@app.get("/health")
def health():
    return {"ok": True, "time": time.time()}


@app.post("/invoke")
def invoke(req: InvokeReq):
    run_id = str(uuid.uuid4())
    # This is a template: wire to OpenClaw, agents, tools, etc.
    return {"ok": True, "run_id": run_id, "echo": req.prompt}
