from __future__ import annotations

from dataclasses import dataclass

from .agents.echo_agent import EchoAgent
from .verifier import SimpleVerifier


@dataclass
class AgentInfo:
    agent_id: str
    version: str
    price_per_use: float


def build_registry():
    # Default local agents (extend later)
    safe = SimpleVerifier(prohibited=["password", "token", "api key"])
    agents = {
        "echo": EchoAgent(agent_id="echo", version="0.1.0", price_per_use=0.0, verifier=safe)
    }
    return agents
