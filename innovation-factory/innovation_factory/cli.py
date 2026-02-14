from __future__ import annotations

import argparse
import json
from pathlib import Path

import re

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

from innovation_factory.models import InnovationCandidate
from innovation_factory.render import render_markdown, render_typst


def cmd_demo(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Demo candidate: harmless, high-level; replace with real sim output later.
    c = InnovationCandidate(
        id="demo-001",
        title="Adaptive Microgrids with Community Incentive Contracts",
        one_liner="A microgrid controller that uses simple incentive contracts to shift demand and stabilize renewables.",
        problem="Renewable-heavy grids face volatility; communities need resilience without expensive overbuild.",
        mechanism_steps=[
            "Measure local generation/consumption in 1–5 minute intervals.",
            "Publish a rolling set of incentive prices for flexible loads (EV charging, HVAC, water heating).",
            "Use a transparent contract rule-set so households can opt-in and predict rewards.",
            "Run a controller that targets frequency/voltage stability while respecting opt-in constraints.",
        ],
        required_inputs=["smart meters", "local controller", "flexible loads", "basic comms"],
        constraints=["requires opt-in participation", "privacy-preserving aggregation needed"],
        failure_modes=["low participation", "communication outages", "perverse incentive edge cases"],
        validation_plan=[
            "Simulate with historical load + solar data.",
            "Pilot on a small neighborhood microgrid with opt-in EV owners.",
            "Measure stability events and participant satisfaction.",
        ],
        risks=["privacy", "equity impacts if incentives favor certain households"],
        tags=["energy", "resilience", "incentives"],
    )

    slug = slugify(c.title)
    post_path = out_dir / f"{slug}.md"
    typ_path = out_dir / f"{slug}.typ"

    post_path.write_text(render_markdown(c), encoding="utf-8")
    typ_path.write_text(render_typst(c), encoding="utf-8")

    (out_dir / f"{slug}.json").write_text(c.model_dump_json(indent=2), encoding="utf-8")

    print(json.dumps({"ok": True, "slug": slug, "post": str(post_path), "typst": str(typ_path)}, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="innovation-factory")
    sub = ap.add_subparsers(dest="cmd", required=True)

    demo = sub.add_parser("demo", help="Generate a demo blueprint (md + typst + json)")
    demo.add_argument("--out", type=Path, default=Path("artifacts"))

    args = ap.parse_args()

    if args.cmd == "demo":
        return cmd_demo(args.out)

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
