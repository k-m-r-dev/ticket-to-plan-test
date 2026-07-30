#!/usr/bin/env python3
"""Mark an ABP run as running or plan_ready (updates meta.json)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("action", choices=["start", "finish"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--tool-calls", type=int, default=None)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    meta_path = args.run_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    if args.action == "start":
        meta["status"] = "running"
        meta["started_at"] = utc_now()
        if args.model:
            meta["model"] = args.model
        if args.notes:
            meta["notes"] = args.notes
    else:
        meta["ended_at"] = utc_now()
        started = meta.get("started_at")
        if started:
            try:
                t0 = datetime.fromisoformat(started)
                t1 = datetime.fromisoformat(meta["ended_at"])
                meta["wall_clock_seconds"] = max(0, int((t1 - t0).total_seconds()))
            except ValueError:
                pass
        if args.tool_calls is not None:
            meta["tool_calls"] = args.tool_calls
        if args.model:
            meta["model"] = args.model
        if args.notes:
            meta["notes"] = (meta.get("notes") or "") + ("\n" + args.notes if meta.get("notes") else args.notes)
        art = args.run_dir / "artifacts"
        files = [str(p.relative_to(args.run_dir)) for p in sorted(art.rglob("*")) if p.is_file()] if art.is_dir() else []
        meta["artifact_paths"] = files
        if not files:
            raise SystemExit("Cannot finish: artifacts/ is empty")
        meta["status"] = "plan_ready"

    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(args.run_dir), "status": meta["status"], "wall_clock_seconds": meta.get("wall_clock_seconds")}, indent=2))


if __name__ == "__main__":
    main()
