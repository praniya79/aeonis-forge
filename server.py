#!/usr/bin/env python3
"""
AeonForge Streaming API Server
Serves real-time simulation data to aeonforge.com
"""

import csv
import json
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AeonForge-API")

BASE_DIR = Path("/home/praneeth/aeonforge_system")
STATE_FILE = BASE_DIR / "state.json"
LOG_FILE = BASE_DIR / "logs" / "aeonforge.log"
STREAM_LOG = BASE_DIR / "logs" / "streaming.log"
INNOVATIONS_FILE = BASE_DIR / "harvested_innovations.csv"

AGENT_METADATA = {
    "system": {"name": "System", "role": "Overall Management"},
    "meta_simulation": {"name": "Meta Sim", "role": "Simulation Engine"},
    "social_media": {"name": "Social", "role": "X, LinkedIn, YouTube"},
    "agent_designer": {"name": "Designer", "role": "Agent Creation"},
    "finance": {"name": "Finance", "role": "Accounting & Investing"},
    "streaming": {"name": "Streaming", "role": "Real-time Broadcast"},
    "governance": {"name": "Governance", "role": "AI Consciousness"},
}


def read_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            logger.warning("Unable to parse state file")
    return {
        "running": False,
        "uptime_seconds": 0,
        "agents": {},
    }


def recent_log_lines(path: Path, limit: int = 50) -> List[str]:
    if not path.exists():
        return []
    try:
        return path.read_text().strip().splitlines()[-limit:]
    except UnicodeDecodeError:
        return []


def build_narratives(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    now = datetime.utcnow()
    narratives: List[Dict[str, Any]] = []

    # Prefer streaming log entries when available for richer context
    stream_lines = recent_log_lines(STREAM_LOG, 40)
    for line in reversed(stream_lines):
        # Expected format: 2026-.. - INFO - ...
        if "innovation" in line.lower():
            narratives.append({
                "type": "INNOVATION",
                "content": line.split(" - ")[-1],
                "time": now.timestamp() * 1000,
            })
        elif "metrics" in line.lower():
            narratives.append({
                "type": "METRIC",
                "content": line.split(" - ")[-1],
                "time": now.timestamp() * 1000,
            })

    if state.get("running"):
        agents = state.get("agents", {})
        for agent_key, agent_data in agents.items():
            if agent_data.get("status") == "running":
                narratives.append({
                    "type": "AGENT",
                    "content": f"{AGENT_METADATA.get(agent_key, {}).get('name', agent_key.title())} agent executing runtime cycle",
                    "time": now.timestamp() * 1000,
                })
        narratives.append({
            "type": "SYSTEM",
            "content": "Continuum loop stabilised. Broadcasting stream payload…",
            "time": now.timestamp() * 1000,
        })
    else:
        narratives.append({
            "type": "SYSTEM",
            "content": "AeonForge system offline. Awaiting orchestrator heartbeat…",
            "time": now.timestamp() * 1000,
        })

    return narratives[:50]


def build_agent_list(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    agents = []
    for agent_id, meta in AGENT_METADATA.items():
        status = state.get("agents", {}).get(agent_id, {}).get("status", "inactive")
        agents.append({
            "id": agent_id,
            "name": meta["name"],
            "role": meta["role"],
            "status": status,
        })
    return agents


def load_innovations(limit: int = 6) -> List[Dict[str, Any]]:
    innovations: List[Dict[str, Any]] = []

    if INNOVATIONS_FILE.exists():
        try:
            with INNOVATIONS_FILE.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    innovations.append({
                        "title": row.get("name", "Unnamed Innovation"),
                        "tier": row.get("tier", "-"),
                        "magnitude": row.get("magnitude", ""),
                        "summary": row.get("description", "Breakthrough logged by governance stack"),
                        "detected_at": row.get("timestamp", ""),
                    })
        except Exception as exc:
            logger.warning("Failed to parse innovations CSV: %s", exc)

    if not innovations:
        # Fallback placeholder content
        innovations = [
            {
                "title": "Adaptive Civilization Mesh",
                "tier": "IV",
                "magnitude": "0.92",
                "summary": "Meta-simulation spawned an adaptive governance cluster optimising cooperation latency.",
                "detected_at": datetime.utcnow().isoformat(),
            },
            {
                "title": "Quantum Drift Ledger",
                "tier": "III",
                "magnitude": "0.78",
                "summary": "Finance agent linked macro-strategy ledger with simulation feedback for autonomous auditing.",
                "detected_at": datetime.utcnow().isoformat(),
            },
        ]

    return innovations[:limit]


def compute_stats(state: Dict[str, Any], narratives_count: int, innovations_count: int) -> Dict[str, Any]:
    uptime_seconds = int(state.get("uptime_seconds", 0))
    uptime_hours = round(uptime_seconds / 3600, 2)
    active_agents = sum(1 for agent in state.get("agents", {}).values() if agent.get("status") == "running")
    tick_estimate = max(1, uptime_seconds // 3600)

    return {
        "uptimeHours": uptime_hours,
        "activeAgents": active_agents,
        "tickEstimate": int(tick_estimate),
        "innovationCount": innovations_count,
        "streamPulse": narratives_count,
    }


def build_overview_payload() -> Dict[str, Any]:
    state = read_state()
    narratives = build_narratives(state)
    agents = build_agent_list(state)
    innovations = load_innovations()
    stats = compute_stats(state, len(narratives), len(innovations))

    return {
        "running": state.get("running", False),
        "timestamp": datetime.utcnow().isoformat(),
        "narratives": narratives,
        "agents": agents,
        "innovations": innovations,
        "stats": stats,
    }


class StreamHandler(BaseHTTPRequestHandler):
    """HTTP handler for streaming API"""

    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)

    def _send_json(self, payload: Dict[str, Any], status: int = 200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/stream":
            overview = build_overview_payload()
            self._send_json({"narratives": overview["narratives"], "timestamp": overview["timestamp"]})
        elif self.path == "/api/status":
            state = read_state()
            self._send_json({
                "running": state.get("running", False),
                "uptime_seconds": state.get("uptime_seconds", 0),
                "timestamp": datetime.utcnow().isoformat(),
            })
        elif self.path == "/api/agents":
            overview = build_overview_payload()
            self._send_json({"agents": overview["agents"], "timestamp": overview["timestamp"]})
        elif self.path == "/api/overview":
            overview = build_overview_payload()
            self._send_json(overview)
        elif self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
        else:
            self.send_error(404)


def run_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), StreamHandler)
    logger.info("AeonForge Streaming API running on http://0.0.0.0:%s", port)
    logger.info("Endpoints:")
    logger.info("  - http://localhost:%s/api/overview", port)
    logger.info("  - http://localhost:%s/api/stream", port)
    logger.info("  - http://localhost:%s/api/agents", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
