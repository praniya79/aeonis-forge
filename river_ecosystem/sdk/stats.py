import json
import os
import time
from typing import Any


class MarketStats:
    """Append-only JSONL ledger + in-memory totals."""

    def __init__(self, out_path: str):
        self.out_path = out_path
        self._seen: set[str] = set()
        self.app_revenue: dict[str, float] = {}

    def record_task(self, user_id: str, agent_id: str, cost: float, task_id: str | None = None, **meta: Any) -> dict[str, Any]:
        ts = time.time()

        if task_id:
            if task_id in self._seen:
                return {"ok": True, "deduped": True, "task_id": task_id}
            self._seen.add(task_id)

        cost_f = float(cost)
        self.app_revenue[agent_id] = float(self.app_revenue.get(agent_id, 0.0)) + cost_f

        rec = {
            "ts": ts,
            "user_id": str(user_id),
            "agent_id": str(agent_id),
            "cost": cost_f,
            **meta,
        }

        os.makedirs(os.path.dirname(self.out_path) or ".", exist_ok=True)
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        return rec
