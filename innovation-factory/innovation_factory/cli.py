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
from innovation_factory import db


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

    # Optional: also drop into MkDocs site if present
    mkdocs_posts = Path(__file__).resolve().parents[2] / "site" / "docs" / "posts"
    if mkdocs_posts.exists():
        (mkdocs_posts / f"{slug}.md").write_text(render_markdown(c), encoding="utf-8")

    print(json.dumps({"ok": True, "slug": slug, "post": str(post_path), "typst": str(typ_path)}, indent=2))
    return 0


def cmd_init(db_path: Path) -> int:
    db.init(db_path)
    print(json.dumps({"ok": True, "db": str(db_path)}, indent=2))
    return 0


def cmd_ingest(db_path: Path, json_path: Path) -> int:
    db.init(db_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    c = InnovationCandidate.model_validate(payload)

    con = db.connect(db_path)
    try:
        con.execute(
            "INSERT OR REPLACE INTO candidates(id,title,one_liner,problem,json,created_at,source) VALUES (?,?,?,?,?,?,?)",
            (
                c.id,
                c.title,
                c.one_liner,
                c.problem,
                c.model_dump_json(),
                c.created_at.isoformat(),
                c.source,
            ),
        )
        con.commit()
    finally:
        con.close()

    print(json.dumps({"ok": True, "ingested": c.id, "db": str(db_path)}, indent=2))
    return 0


def cmd_queue(db_path: Path, limit: int) -> int:
    db.init(db_path)
    con = db.connect(db_path)
    try:
        rows = con.execute(
            """
            SELECT c.id, c.title, c.created_at
            FROM candidates c
            LEFT JOIN approvals a ON a.candidate_id = c.id
            WHERE a.candidate_id IS NULL
            ORDER BY c.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        con.close()

    out = [{"id": r[0], "title": r[1], "created_at": r[2]} for r in rows]
    print(json.dumps({"ok": True, "pending": out}, indent=2))
    return 0


def cmd_approve(db_path: Path, candidate_id: str, by: str) -> int:
    db.init(db_path)
    con = db.connect(db_path)
    try:
        row = con.execute("SELECT json FROM candidates WHERE id=?", (candidate_id,)).fetchone()
        if not row:
            raise SystemExit(f"candidate not found: {candidate_id}")
        payload = json.loads(row[0])
        c = InnovationCandidate.model_validate(payload)

        # publish to site
        slug = slugify(c.title)
        mkdocs_posts = Path(__file__).resolve().parents[2] / "site" / "docs" / "posts"
        mkdocs_posts.mkdir(parents=True, exist_ok=True)
        post_path = mkdocs_posts / f"{slug}.md"
        post_path.write_text(render_markdown(c), encoding="utf-8")

        con.execute(
            "INSERT OR REPLACE INTO approvals(candidate_id, approved_at, approved_by, status) VALUES (?,?,?,?)",
            (candidate_id, __import__("datetime").datetime.utcnow().isoformat(), by, "approved"),
        )
        con.execute(
            "INSERT INTO publish_log(candidate_id, published_at, target, detail) VALUES (?,?,?,?)",
            (candidate_id, __import__("datetime").datetime.utcnow().isoformat(), "mkdocs", str(post_path)),
        )
        con.commit()
    finally:
        con.close()

    print(json.dumps({"ok": True, "approved": candidate_id, "post": str(post_path)}, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="innovation-factory")
    sub = ap.add_subparsers(dest="cmd", required=True)

    demo = sub.add_parser("demo", help="Generate a demo blueprint (md + typst + json)")
    demo.add_argument("--out", type=Path, default=Path("artifacts"))

    initp = sub.add_parser("init", help="Initialize the SQLite database")
    initp.add_argument("--db", type=Path, default=Path("..") / "data" / "aeonis_forge.db")

    ingest = sub.add_parser("ingest", help="Ingest a candidate JSON into the database")
    ingest.add_argument("json", type=Path)
    ingest.add_argument("--db", type=Path, default=Path("..") / "data" / "aeonis_forge.db")

    queue = sub.add_parser("queue", help="List pending candidates")
    queue.add_argument("--db", type=Path, default=Path("..") / "data" / "aeonis_forge.db")
    queue.add_argument("--limit", type=int, default=10)

    approve = sub.add_parser("approve", help="Approve and publish a candidate into the site")
    approve.add_argument("id", help="Candidate id")
    approve.add_argument("--by", default="prana")
    approve.add_argument("--db", type=Path, default=Path("..") / "data" / "aeonis_forge.db")

    args = ap.parse_args()

    if args.cmd == "demo":
        return cmd_demo(args.out)
    if args.cmd == "init":
        return cmd_init(args.db)
    if args.cmd == "ingest":
        return cmd_ingest(args.db, args.json)
    if args.cmd == "queue":
        return cmd_queue(args.db, args.limit)
    if args.cmd == "approve":
        return cmd_approve(args.db, args.id, args.by)

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
