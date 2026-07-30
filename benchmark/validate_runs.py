#!/usr/bin/env python3
"""Validate ABP run meta completeness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parent
REQUIRED_WHEN_READY = ["started_at", "ended_at", "wall_clock_seconds", "tool_calls"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    args = ap.parse_args()
    base = BENCH / "runs" / args.protocol
    ok = 0
    pending = 0
    bad = []
    for meta_path in sorted(base.rglob("meta.json")):
        if "execute" in meta_path.parts or "human_sheets" in meta_path.parts:
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        status = meta.get("status")
        if status == "awaiting_operator":
            pending += 1
            continue
        missing = [k for k in REQUIRED_WHEN_READY if meta.get(k) is None]
        art = meta_path.parent / "artifacts"
        files = list(art.rglob("*")) if art.is_dir() else []
        if missing or not any(f.is_file() for f in files):
            bad.append((str(meta_path), missing, len(files)))
        else:
            ok += 1
    print(json.dumps({"ok": ok, "awaiting_operator": pending, "bad": bad}, indent=2))
    if bad:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
