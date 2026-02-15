from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS candidates (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  one_liner TEXT NOT NULL,
  problem TEXT NOT NULL,
  json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
  candidate_id TEXT PRIMARY KEY,
  novelty REAL NOT NULL,
  coherence REAL NOT NULL,
  feasibility REAL NOT NULL,
  safety REAL NOT NULL,
  overall REAL NOT NULL,
  decision TEXT NOT NULL,
  flagged INTEGER NOT NULL,
  notes TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);

CREATE TABLE IF NOT EXISTS approvals (
  candidate_id TEXT PRIMARY KEY,
  approved_at TEXT NOT NULL,
  approved_by TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);

CREATE TABLE IF NOT EXISTS publish_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  candidate_id TEXT NOT NULL,
  published_at TEXT NOT NULL,
  target TEXT NOT NULL,
  detail TEXT NOT NULL,
  FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    con.execute("PRAGMA foreign_keys=ON;")
    return con


def init(db_path: Path) -> None:
    con = connect(db_path)
    try:
        con.executescript(SCHEMA)
        con.commit()
    finally:
        con.close()


def rows(con: sqlite3.Connection, sql: str, params: Iterable | None = None):
    cur = con.execute(sql, params or [])
    return cur.fetchall()
