from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class InnovationCandidate(BaseModel):
    id: str
    title: str
    one_liner: str
    problem: str
    mechanism_steps: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    validation_plan: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    # provenance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source: str = "demo"  # later: sim-run id, seed, agent versions


class ReviewResult(BaseModel):
    novelty: float = 0.0
    coherence: float = 0.0
    feasibility: float = 0.0
    safety: float = 0.0
    overall: float = 0.0
    notes: list[str] = Field(default_factory=list)

    decision: Literal["approve", "reject", "revise", "hold"] = "hold"
    flagged: bool = False
    flagged_reasons: list[str] = Field(default_factory=list)


class RenderResult(BaseModel):
    slug: str
    post_md_path: str
    typst_path: Optional[str] = None
    pdf_path: Optional[str] = None
