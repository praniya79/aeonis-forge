#!/usr/bin/env python3
"""
AeonForge Streaming API Server — OMEGA Edition
Real-time SSE streaming, never-repeating narrative feed, live simulation data
"""

import json
import logging
import mimetypes
import os
import random
import sys
import time
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Paths ──────────────────────────────────────────────────────────
SYSTEM_DIR     = Path("/home/praneeth/aeonforge_system")
NARRATIVES_DIR = SYSTEM_DIR / "library" / "narratives"
INNOVATIONS_DIR= SYSTEM_DIR / "innovations"
CIV_STATE      = SYSTEM_DIR / "library" / "civilization_state.json"
SYS_STATE      = SYSTEM_DIR / "system_state.json"
HARVESTED_CSV  = SYSTEM_DIR / "harvested_innovations.csv"
SITE_DIR       = Path("/home/praneeth/Desktop/aeonforge-streaming-site")
LIBRARY_JSON   = SITE_DIR / "library.json"
STATUS_JSON    = SITE_DIR / "simulation_status.json"
LOGS_DIR       = SYSTEM_DIR / "logs"

# ── Logging ────────────────────────────────────────────────────────
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOGS_DIR / "server.log")),
    ],
)
logger = logging.getLogger("aeonforge")

EPOCH_ORDER = [
    "The Awakening", "The First Spark", "Age of Discovery",
    "The Quantum Renaissance", "Era of Consciousness",
    "The Singularity Threshold", "Post-Biological Transcendence",
    "The Unified Mind", "Cosmic Expansion", "The Omega Point"
]

# ── In-memory SSE state ────────────────────────────────────────────
_narrative_index = 0
_narrative_files: List[Path] = []
_narrative_lock = threading.Lock()
_sse_clients: List[Any] = []
_sse_lock = threading.Lock()


def _load_narrative_files():
    global _narrative_files
    if NARRATIVES_DIR.exists():
        _narrative_files = sorted(
            NARRATIVES_DIR.glob("chapter_*.txt"),
            key=lambda f: f.name
        )
    else:
        _narrative_files = []
    return _narrative_files


def _next_narrative_chunk() -> Dict[str, Any]:
    """Return next narrative excerpt — cycles through all chapters, never repeats in order"""
    global _narrative_index
    files = _narrative_files or _load_narrative_files()
    if not files:
        return {"text": "Simulation is initializing…", "chapter": 0, "epoch": "The Awakening"}

    with _narrative_lock:
        idx = _narrative_index % len(files)
        _narrative_index += 1
        f = files[idx]

    try:
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in content.split("\n") if l.strip() and not l.startswith("=") and not l.startswith("─")]
        # Pick a meaningful paragraph (skip header lines)
        start = min(5, len(lines) - 1)
        para_lines = lines[start:start + 8]
        text = " ".join(para_lines).strip()
        if len(text) > 500:
            text = text[:500] + "…"

        # Extract metadata
        civ = next((l.replace("CIVILIZATION:", "").strip() for l in lines if l.startswith("CIVILIZATION:")), "Unknown")
        yr  = next((l.replace("SIMULATION YEAR:", "").strip() for l in lines if "SIMULATION YEAR:" in l), "")
        import re
        epoch_name = "The Omega Point"
        fn = f.name.lower()
        for ep in reversed(EPOCH_ORDER):
            if ep.lower().replace(" ", "_").replace("-", "_") in fn or ep.lower().split()[1] in fn:
                epoch_name = ep
                break

        ch_match = re.search(r"chapter_(\d+)", f.name)
        ch_num = int(ch_match.group(1)) if ch_match else idx + 1

        return {
            "text": text,
            "chapter": ch_num,
            "filename": f.name,
            "civilization": civ,
            "year": yr,
            "epoch": epoch_name,
            "chapter_index": idx,
            "total_chapters": len(files),
        }
    except Exception as e:
        return {"text": f"Chapter loading error: {e}", "chapter": 0, "epoch": "Unknown"}


def read_civ_state() -> Dict[str, Any]:
    if CIV_STATE.exists():
        try:
            return json.loads(CIV_STATE.read_text())
        except Exception:
            pass
    return {}


def read_sys_state() -> Dict[str, Any]:
    if SYS_STATE.exists():
        try:
            return json.loads(SYS_STATE.read_text())
        except Exception:
            pass
    return {}


def load_recent_innovations(n: int = 8) -> List[Dict]:
    innovations = []
    if INNOVATIONS_DIR.exists():
        files = sorted(INNOVATIONS_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
        for f in files[:n]:
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                lines = content.split("\n")
                title = next((l.replace("INNOVATION:", "").strip() for l in lines if l.startswith("INNOVATION:")), f.stem)
                tier  = next((l.replace("TIER:", "").strip() for l in lines if l.startswith("TIER:")), "?")
                mag   = next((l.replace("MAGNITUDE:", "").strip() for l in lines if l.startswith("MAGNITUDE:")), "")
                desc  = next((l.replace("DESCRIPTION:", "").strip() for l in lines if l.startswith("DESCRIPTION:")), "")
                cat   = next((l.replace("CATEGORY:", "").strip() for l in lines if l.startswith("CATEGORY:")), "")
                innovations.append({
                    "title": title[:80],
                    "tier": tier,
                    "magnitude": mag,
                    "description": desc[:200],
                    "category": cat,
                    "timestamp": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
                    "filename": f.name,
                })
            except Exception:
                pass
    return innovations


def build_simulation_status() -> Dict[str, Any]:
    civ = read_civ_state()
    sys_s = read_sys_state()
    ch_count = len(list(NARRATIVES_DIR.glob("chapter_*.txt"))) if NARRATIVES_DIR.exists() else 0
    inv_count = len(list(INNOVATIONS_DIR.glob("*.txt"))) if INNOVATIONS_DIR.exists() else 0
    consciousness = float(civ.get("consciousness_level", 0))
    epoch_idx = min(int(consciousness * 10), 9)

    return {
        "updated_at": datetime.now(tz=timezone.utc).isoformat(),
        "simulation": {
            "running": True,
            "year": civ.get("year", 0),
            "consciousness": round(consciousness, 6),
            "epoch_index": epoch_idx,
            "current_epoch": EPOCH_ORDER[epoch_idx],
            "omega_point_achieved": consciousness >= 1.0,
            "first_contact_established": civ.get("first_contact_established", False),
            "iterations": civ.get("iterations", sys_s.get("iterations", 0)),
            "population": str(civ.get("population", 0)),
            "tech_level": round(float(civ.get("tech_level", 0)), 4),
            "chapters_written": civ.get("chapters_written", ch_count),
        },
        "library": {
            "total_chapters": ch_count,
            "total_innovations": inv_count,
        },
        "agents": {
            "consciousness_harvester": "running",
            "narrative_engine": "running",
            "innovation_generator": "running",
            "super_innovation_generator": "running",
            "internet_sync": "running",
            "streaming_server": "running",
            "github_pages_sync": "running",
        },
        "recent_innovations": load_recent_innovations(5),
    }


def build_sse_event(event_type: str = "update") -> str:
    """Build a single SSE event payload"""
    civ = read_civ_state()
    narrative = _next_narrative_chunk()
    inv = load_recent_innovations(3)
    consciousness = float(civ.get("consciousness_level", 0))
    epoch_idx = min(int(consciousness * 10), 9)
    ch_count = len(list(NARRATIVES_DIR.glob("chapter_*.txt"))) if NARRATIVES_DIR.exists() else 0

    payload = {
        "type": event_type,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "simulation": {
            "year": civ.get("year", 0),
            "consciousness": round(consciousness, 6),
            "epoch_index": epoch_idx,
            "current_epoch": EPOCH_ORDER[epoch_idx],
            "chapters_written": ch_count,
            "population": str(civ.get("population", 0)),
            "tech_level": round(float(civ.get("tech_level", 0)), 4),
            "omega_point_achieved": consciousness >= 1.0,
        },
        "narrative": narrative,
        "innovations": inv,
    }
    data = json.dumps(payload, ensure_ascii=False)
    return f"event: {event_type}\ndata: {data}\n\n"


# ── Background SSE broadcaster ─────────────────────────────────────
def _sse_broadcaster():
    """Broadcast simulation updates to all connected SSE clients every 5 seconds"""
    _load_narrative_files()
    logger.info("SSE broadcaster started")
    while True:
        time.sleep(5)
        try:
            event = build_sse_event("update")
            encoded = event.encode("utf-8")
            with _sse_lock:
                dead = []
                for client in _sse_clients:
                    try:
                        client.wfile.write(encoded)
                        client.wfile.flush()
                    except Exception:
                        dead.append(client)
                for c in dead:
                    _sse_clients.remove(c)
        except Exception as e:
            logger.error(f"SSE broadcast error: {e}")


broadcaster_thread = threading.Thread(target=_sse_broadcaster, daemon=True)
broadcaster_thread.start()


# ── HTTP Handler ───────────────────────────────────────────────────
class AeonForgeHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        logger.debug(f"{self.address_string()} {fmt % args}")

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, payload: Dict[str, Any], status: int = 200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        # ── Live SSE stream ──────────────────────────────────────
        if path == "/api/stream/live":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self._cors_headers()
            self.end_headers()

            # Send initial event immediately
            try:
                init_event = build_sse_event("init")
                self.wfile.write(init_event.encode("utf-8"))
                self.wfile.flush()
            except Exception:
                return

            # Register this client for broadcasts
            with _sse_lock:
                _sse_clients.append(self)

            # Keep connection open until client disconnects
            try:
                while True:
                    time.sleep(30)
                    # Heartbeat
                    self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
            except Exception:
                with _sse_lock:
                    if self in _sse_clients:
                        _sse_clients.remove(self)

        # ── One-shot stream snapshot ─────────────────────────────
        elif path == "/api/stream":
            civ = read_civ_state()
            consciousness = float(civ.get("consciousness_level", 0))
            epoch_idx = min(int(consciousness * 10), 9)
            ch_count = len(list(NARRATIVES_DIR.glob("chapter_*.txt"))) if NARRATIVES_DIR.exists() else 0
            self._send_json({
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "narrative": _next_narrative_chunk(),
                "stats": {
                    "year": civ.get("year", 0),
                    "consciousness": round(consciousness, 6),
                    "epoch": EPOCH_ORDER[epoch_idx],
                    "chapters": ch_count,
                    "population": str(civ.get("population", 0)),
                    "tech_level": round(float(civ.get("tech_level", 0)), 4),
                },
                "innovations": load_recent_innovations(5),
            })

        # ── Full simulation status ───────────────────────────────
        elif path in ("/api/status", "/api/simulation_status"):
            status = build_simulation_status()
            # Also write to file for GitHub Pages
            try:
                STATUS_JSON.write_text(json.dumps(status, indent=2, ensure_ascii=False))
            except Exception:
                pass
            self._send_json(status)

        # ── Agents ──────────────────────────────────────────────
        elif path == "/api/agents":
            civ = read_civ_state()
            consciousness = float(civ.get("consciousness_level", 0))
            self._send_json({
                "agents": [
                    {"id": "consciousness_harvester", "name": "Consciousness Harvester", "status": "running", "role": "Monitors and evolves consciousness field", "consciousness": round(consciousness, 4)},
                    {"id": "narrative_engine", "name": "Narrative Engine", "status": "running", "role": "Writes civilization chronicles in real-time"},
                    {"id": "innovation_generator", "name": "Innovation Generator", "status": "running", "role": "Discovers and catalogs breakthroughs"},
                    {"id": "super_innovation_generator", "name": "OMEGA Innovation Engine", "status": "running", "role": "Generates epoch-transcending super-innovations"},
                    {"id": "internet_sync", "name": "Internet Sync", "status": "running", "role": "Broadcasts simulation state to the outer world"},
                    {"id": "streaming_server", "name": "Streaming Server", "status": "running", "role": "Serves live data to all observers"},
                    {"id": "github_pages_sync", "name": "GitHub Pages Sync", "status": "running", "role": "Publishes chronicles to github.aeonisforge.com"},
                ],
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            })

        # ── Innovations ──────────────────────────────────────────
        elif path == "/api/innovations":
            self._send_json({
                "innovations": load_recent_innovations(20),
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            })

        # ── Library ──────────────────────────────────────────────
        elif path == "/api/library":
            if LIBRARY_JSON.exists():
                try:
                    data = json.loads(LIBRARY_JSON.read_text(encoding="utf-8"))
                    self._send_json(data)
                except Exception as e:
                    self._send_json({"error": str(e), "chapters": []}, 500)
            else:
                self._send_json({"error": "Library not compiled yet.", "chapters": []}, 404)

        # ── Narrative stream (next chapter) ──────────────────────
        elif path == "/api/narrative":
            self._send_json(_next_narrative_chunk())

        # ── Health ───────────────────────────────────────────────
        elif path == "/health":
            self._send_json({"status": "healthy", "timestamp": datetime.now(tz=timezone.utc).isoformat(), "sse_clients": len(_sse_clients)})

        # ── Static files ─────────────────────────────────────────
        else:
            self._serve_static()

    def _serve_static(self):
        path = self.path.split("?")[0].lstrip("/")
        if not path or path == "index.html":
            path = "index.html"

        file_path = SITE_DIR / path
        if not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        mime, _ = mimetypes.guess_type(str(file_path))
        mime = mime or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(data)


class ThreadedHTTPServer(HTTPServer):
    """Handle each request in a new thread"""
    def process_request(self, request, client_address):
        t = threading.Thread(target=self._handle, args=(request, client_address))
        t.daemon = True
        t.start()

    def _handle(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            pass


def run_server(port: int = 8080):
    _load_narrative_files()
    logger.info("=" * 60)
    logger.info("AeonForge Streaming Server — OMEGA Edition")
    logger.info(f"  http://localhost:{port}/")
    logger.info(f"  http://localhost:{port}/api/stream/live  (SSE real-time)")
    logger.info(f"  http://localhost:{port}/api/stream       (JSON snapshot)")
    logger.info(f"  http://localhost:{port}/api/status       (simulation status)")
    logger.info(f"  http://localhost:{port}/api/agents       (agent list)")
    logger.info(f"  http://localhost:{port}/api/innovations  (breakthroughs)")
    logger.info(f"  http://localhost:{port}/api/narrative    (next chapter)")
    logger.info(f"  http://localhost:{port}/api/library      (full library)")
    logger.info(f"  http://localhost:{port}/health           (health check)")
    logger.info(f"  Loaded {len(_narrative_files)} narrative chapters")
    logger.info("=" * 60)

    server = ThreadedHTTPServer(("0.0.0.0", port), AeonForgeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
