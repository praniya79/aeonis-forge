from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..verifier import SimpleVerifier


@dataclass
class AgentResponse:
    text: str
    meta: dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    def __init__(self, agent_id: str, version: str = "0.0.0", price_per_use: float = 0.0, verifier=None):
        self.agent_id = agent_id
        self.version = version
        self.price_per_use = float(price_per_use)
        self.verifier = verifier or SimpleVerifier([])

    def identity(self) -> tuple[str, str]:
        return self.agent_id, self.version

    def run(self, prompt: str, **kwargs) -> AgentResponse:
        raise NotImplementedError

    def safe_run(self, prompt: str, **kwargs) -> AgentResponse:
        resp = self.run(prompt, **kwargs)
        self.verifier.verify_or_raise(resp.text)
        resp.meta.setdefault("agent_id", self.agent_id)
        resp.meta.setdefault("version", self.version)
        return resp
