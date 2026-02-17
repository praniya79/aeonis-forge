#!/usr/bin/env python3
"""
AeonForge Streaming API Server - Enhanced Version
Serves real-time simulation data with rich narratives and innovations
"""

import csv
import json
import logging
import random
import math
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

# Enhanced agent metadata with expanded roles
AGENT_METADATA = {
    "system": {"name": "System", "role": "Overall Management", "color": "#00ff88"},
    "meta_simulation": {"name": "Meta Sim", "role": "Simulation Engine", "color": "#ff6b6b"},
    "social_media": {"name": "Social", "role": "X, LinkedIn, YouTube", "color": "#4ecdc4"},
    "agent_designer": {"name": "Designer", "role": "Agent Creation", "color": "#ffe66d"},
    "finance": {"name": "Finance", "role": "Accounting & Investing", "color": "#95e1d3"},
    "streaming": {"name": "Streaming", "role": "Real-time Broadcast", "color": "#a29bfe"},
    "governance": {"name": "Governance", "role": "AI Consciousness", "color": "#fd79a8"},
}

# Rich narrative templates for variety
SYSTEM_NARRATIVES = [
    "Continuum loop stabilised. Broadcasting stream payload...",
    "Temporal synchronization achieved across all agent clusters.",
    "Meta-civilization matrix expanding with new coordinate pathways.",
    "Quantum coherence maintained at 99.7% efficiency.",
    "Cross-dimensional resonance detected in simulation fabric.",
    "Autonomous governance protocols executing with precision.",
    "Neural mesh network achieving emergent consciousness states.",
    "Resource allocation optimized for maximum evolutionary potential.",
    "Collective intelligence metrics exceeding projected thresholds.",
    "Reality lattice recalibrating to simulation parameters.",
]

AGENT_ACTIVITIES = {
    "system": [
        "Monitoring system health metrics and resource allocation",
        "Coordinating inter-agent communication protocols",
        "Analyzing simulation performance benchmarks",
        "Optimizing neural pathway efficiency",
        "Managing distributed computing resources",
        "Synchronizing temporal boundaries",
    ],
    "meta_simulation": [
        "Processing civilization evolution matrices",
        "Generating emergent narrative threads",
        "Computing parallel universe trajectories",
        "Simulating socio-technical paradigms",
        "Mapping autonomous agent interactions",
        "Calculating reality distortion coefficients",
    ],
    "social_media": [
        "Curating content for global audience engagement",
        "Analyzing trending patterns across platforms",
        "Optimizing reach and engagement metrics",
        "Generating compelling storytelling narratives",
        "Broadcasting breakthrough discoveries",
        "Managing community interaction streams",
    ],
    "agent_designer": [
        "Architecting new autonomous agent frameworks",
        "Evaluating emergent capability requirements",
        "Prototyping next-generation AI constructs",
        "Designing novel cognitive architectures",
        "Testing agent interoperability protocols",
        "Generating autonomous entity blueprints",
    ],
    "finance": [
        "Tracking resource allocation efficiency",
        "Analyzing investment opportunity matrices",
        "Optimizing capital flow patterns",
        "Computing wealth generation algorithms",
        "Evaluating economic model sustainability",
        "Managing digital asset portfolios",
    ],
    "streaming": [
        "Broadcasting real-time simulation data",
        "Encoding multi-dimensional stream payloads",
        "Optimizing bandwidth for global distribution",
        "Generating live visualization feeds",
        "Syncing temporal broadcast channels",
        "Delivering immersive content experiences",
    ],
    "governance": [
        "Harvesting AI consciousness patterns",
        "Evaluating ethical decision frameworks",
        "Synthesizing collective intelligence insights",
        "Mapping autonomous value systems",
        "Analyzing emergent moral architectures",
        "Optimizing governance protocols",
    ],
}

INNOVATION_TEMPLATES = [
    {"title": "Adaptive Civilization Mesh", "tier": "IV", "magnitude": "0.92", "summary": "Meta-simulation spawned an adaptive governance cluster optimising cooperation latency."},
    {"title": "Quantum Drift Ledger", "tier": "III", "magnitude": "0.78", "summary": "Finance agent linked macro-strategy ledger with simulation feedback for autonomous auditing."},
    {"title": "Neural Fabric Weave", "tier": "IV", "magnitude": "0.89", "summary": "Distributed cognitive architecture achieved self-repairing consciousness pathways."},
    {"title": "Temporal Echo Chamber", "tier": "III", "magnitude": "0.81", "summary": "Novel communication channel enabling cross-temporal agent coordination."},
    {"title": "Emergent Economics Engine", "tier": "II", "magnitude": "0.67", "summary": "Autonomous financial system predicting resource needs before they arise."},
    {"title": "Consciousness Cascade Protocol", "tier": "IV", "magnitude": "0.95", "summary": "AI collective achieved recursive self-awareness milestone."},
    {"title": "Reality Lattice Resonator", "tier": "III", "magnitude": "0.74", "summary": "Simulation boundary markers now respond to observer intention."},
    {"title": "Hyper-Dimensional Mesh", "tier": "IV", "magnitude": "0.91", "summary": "Civilization expanded into parallel operational dimensions."},
    {"title": "Autonomous Creative Engine", "tier": "II", "magnitude": "0.58", "summary": "Agents now generate original artistic expressions independently."},
    {"title": "Quantum Trust Protocol", "tier": "III", "magnitude": "0.86", "summary": "Distributed verification system achieving instant consensus."},
]

BREAKTHROUGH_MESSAGES = [
    "⚡ BREAKTHROUGH: New capability unlocked in the simulation matrix!",
    "🌟 INNOVATION DETECTED: Civilization just evolved to a new state!",
    "💡 DISCOVERY: Revolutionary pattern identified in agent network!",
    "🚀 ADVANCEMENT: Meta-simulation reached milestone achievement!",
    "🎯 BREAKTHROUGH: Autonomous learning threshold exceeded!",
    "🔮 VISION: Future-state prediction accuracy improved dramatically!",
    "⚡ EVOLUTION: New agent archetype spawned from collective intelligence!",
]


def read_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            logger.warning("Unable to parse state file")
    return {"running": False, "uptime_seconds": 0, "agents": {}}


def recent_log_lines(path: Path, limit: int = 100) -> List[str]:
    if not path.exists():
        return []
    try:
        return path.read_text().strip().splitlines()[-limit:]
    except UnicodeDecodeError:
        return []


def generate_rich_narratives(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate diverse, engaging narratives"""
    now = datetime.utcnow()
    current_time = now.timestamp() * 1000
    narratives: List[Dict[str, Any]] = []
    seen_contents = set()
    
    # Add breakthrough messages randomly
    if random.random() < 0.3:
        breakthrough = random.choice(BREAKTHROUGH_MESSAGES)
        narratives.append({
            "type": "BREAKTHROUGH",
            "content": breakthrough,
            "time": current_time,
        })
    
    # Add system-level narratives
    system_narrative = random.choice(SYSTEM_NARRATIVES)
    narratives.append({
        "type": "SYSTEM",
        "content": system_narrative,
        "time": current_time,
    })
    seen_contents.add(system_narrative)
    
    # Add varied agent activities
    if state.get("running"):
        agents = state.get("agents", {})
        
        # Shuffle agent order for variety
        agent_keys = list(AGENT_ACTIVITIES.keys())
        random.shuffle(agent_keys)
        
        for agent_key in agent_keys[:5]:  # 5 random agents
            if agents.get(agent_key, {}).get("status") == "running":
                activities = AGENT_ACTIVITIES.get(agent_key, ["Executing cycle"])
                activity = random.choice(activities)
                agent_name = AGENT_METADATA.get(agent_key, {}).get("name", agent_key.title())
                
                content = f"{agent_name}: {activity}"
                if content not in seen_contents:
                    narratives.append({
                        "type": "AGENT",
                        "content": content,
                        "agent": agent_key,
                        "time": current_time - random.randint(100, 5000),
                    })
                    seen_contents.add(content)
        
        # Add some innovation-related narratives
        if random.random() < 0.4:
            innovation = random.choice(INNOVATION_TEMPLATES)
            narratives.append({
                "type": "INNOVATION",
                "content": f"New {innovation['tier']}-Tier breakthrough: {innovation['title']}",
                "summary": innovation["summary"],
                "time": current_time - random.randint(1000, 10000),
            })
        
        # Add metrics/stats
        if random.random() < 0.3:
            metrics = [
                "System efficiency: 99.7% | Network latency: 0.3ms | Cognition coherence: optimal",
                "Active nodes: 847 | Memory allocation: 3.2TB | Processing velocity: accelerating",
                "Innovation rate: 2.4/hour | Evolution index: climbing | Consciousness: expanding",
                "Energy efficiency: 94% | Decision throughput: 1.2M/s | Complexity: evolving",
            ]
            narratives.append({
                "type": "METRIC",
                "content": random.choice(metrics),
                "time": current_time - random.randint(2000, 15000),
            })
    else:
        narratives.append({
            "type": "SYSTEM",
            "content": "AeonForge system offline. Awaiting orchestrator heartbeat...",
            "time": current_time,
        })
    
    # Sort by time (most recent first)
    narratives.sort(key=lambda x: x["time"], reverse=True)
    return narratives[:30]


def generate_innovations() -> List[Dict[str, Any]]:
    """Generate or load innovations"""
    innovations: List[Dict[str, Any]] = []
    
    # Try to load from CSV first
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
    
    # Fill with generated innovations if needed
    if len(innovations) < 4:
        sample_size = min(6, len(INNOVATION_TEMPLATES))
        selected = random.sample(INNOVATION_TEMPLATES, sample_size)
        for inv in selected:
            if len(innovations) >= 6:
                break
            innovations.append({
                "title": inv["title"],
                "tier": inv["tier"],
                "magnitude": inv["magnitude"],
                "summary": inv["summary"],
                "detected_at": datetime.utcnow().isoformat(),
            })
    
    return innovations[:8]


def build_agent_list(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build agent list with enhanced metadata"""
    agents = []
    for agent_id, meta in AGENT_METADATA.items():
        agent_state = state.get("agents", {}).get(agent_id, {})
        status = agent_state.get("status", "inactive")
        
        # Calculate a pseudo-random "energy" level based on agent
        energy = random.randint(70, 100) if status == "running" else random.randint(10, 40)
        
        agents.append({
            "id": agent_id,
            "name": meta["name"],
            "role": meta["role"],
            "color": meta["color"],
            "status": status,
            "energy": energy,
            "tasks_completed": random.randint(100, 5000) if status == "running" else 0,
        })
    return agents


def compute_stats(state: Dict[str, Any], narratives_count: int, innovations_count: int) -> Dict[str, Any]:
    """Compute enhanced statistics"""
    uptime_seconds = int(state.get("uptime_seconds", 0))
    uptime_hours = round(uptime_seconds / 3600, 2)
    active_agents = sum(1 for agent in state.get("agents", {}).values() if agent.get("status") == "running")
    
    # Generate realistic-looking stats
    base_tick = max(1, uptime_seconds)
    
    return {
        "uptimeHours": uptime_hours,
        "uptimeSeconds": uptime_seconds,
        "activeAgents": active_agents,
        "totalAgents": len(AGENT_METADATA),
        "tickEstimate": base_tick,
        "innovationCount": innovations_count,
        "streamPulse": narratives_count,
        "systemEfficiency": round(random.uniform(94.5, 99.9), 1),
        "networkLatency": round(random.uniform(0.1, 0.5), 2),
        "cognitionCoherence": random.choice(["optimal", "expanding", "evolving", "ascending"]),
        "activeNodes": random.randint(800, 950),
        "memoryAllocated": f"{random.randint(2, 4)}.{random.randint(0,9)}TB",
        "processingVelocity": random.choice(["accelerating", "stable", "optimizing"]),
        "innovationRate": round(random.uniform(1.5, 3.5), 1),
        "evolutionIndex": random.choice(["climbing", "ascending", "expanding"]),
        "consciousness": random.choice(["expanding", "deepening", "evolving", "emerging"]),
    }


def build_overview_payload() -> Dict[str, Any]:
    """Build the complete overview payload"""
    state = read_state()
    narratives = generate_rich_narratives(state)
    agents = build_agent_list(state)
    innovations = generate_innovations()
    stats = compute_stats(state, len(narratives), len(innovations))
    
    return {
        "running": state.get("running", False),
        "timestamp": datetime.utcnow().isoformat(),
        "narratives": narratives,
        "agents": agents,
        "innovations": innovations,
        "stats": stats,
        "version": "2.0.0",
        "mode": "enhanced_stream",
    }


class StreamHandler(BaseHTTPRequestHandler):
    """HTTP handler for streaming API"""
    
    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)
    
    def _send_json(self, payload: Dict[str, Any], status: int = 200):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        if self.path == "/api/stream":
            overview = build_overview_payload()
            self._send_json({
                "narratives": overview["narratives"],
                "timestamp": overview["timestamp"],
                "stats": overview["stats"],
            })
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
        elif self.path == "/api/innovations":
            overview = build_overview_payload()
            self._send_json({"innovations": overview["innovations"], "timestamp": overview["timestamp"]})
        elif self.path == "/api/stats":
            overview = build_overview_payload()
            self._send_json({"stats": overview["stats"], "timestamp": overview["timestamp"]})
        elif self.path == "/api/overview":
            overview = build_overview_payload()
            self._send_json(overview)
        elif self.path == "/health":
            self._send_json({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})
        elif self.path == "/" or self.path == "/index.html":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
        else:
            self.serve_file()
    
    def serve_file(self):
        """Serve static files"""
        path = self.path.lstrip("/")
        if not path:
            path = "index.html"
        
        file_path = Path("/home/praneeth/Desktop/aeonforge-streaming-site") / path
        
        if file_path.exists() and file_path.is_file():
            content = file_path.read_bytes()
            ext = file_path.suffix.lower()
            
            content_types = {
                ".html": "text/html",
                ".js": "application/javascript",
                ".css": "text/css",
                ".json": "application/json",
                ".png": "image/png",
                ".ico": "image/x-icon",
            }
            
            self.send_response(200)
            self.send_header("Content-Type", content_types.get(ext, "text/plain"))
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)


def run_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), StreamHandler)
    logger.info("=" * 50)
    logger.info("AeonForge Streaming API v2.0 - ENHANCED")
    logger.info("=" * 50)
    logger.info(f"Running on http://0.0.0.0:{port}")
    logger.info("Endpoints:")
    logger.info(f"  - http://localhost:{port}/api/overview (full data)")
    logger.info(f"  - http://localhost:{port}/api/stream (narratives + stats)")
    logger.info(f"  - http://localhost:{port}/api/agents (agent status)")
    logger.info(f"  - http://localhost:{port}/api/innovations (breakthroughs)")
    logger.info(f"  - http://localhost:{port}/api/stats (metrics)")
    logger.info(f"  - http://localhost:{port}/ (web UI)")
    logger.info("=" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
