#!/usr/bin/env python3
"""Print the next ABP run that is awaiting_operator (canonical order)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ORDER_FIXTURES = ("f1", "f2")
ORDER_ARMS = ("gsd", "openspec", "no-tools", "native")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    base = BENCH / "runs" / args.protocol
    for fx in ORDER_FIXTURES:
        for arm in ORDER_ARMS:
            for r in (1, 2, 3):
                run_dir = base / fx / arm / f"r{r}"
                meta_path = run_dir / "meta.json"
                if not meta_path.is_file():
                    continue
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if meta.get("status") == "awaiting_operator":
                    payload = {
                        "run_dir": str(run_dir),
                        "prompt": str(run_dir / "prompt.md"),
                        "artifacts": str(run_dir / "artifacts"),
                        "arm": arm,
                        "fixture": fx,
                        "replicate": r,
                        "skill": meta.get("skill"),
                        "status": meta.get("status"),
                    }
                    if args.json:
                        print(json.dumps(payload, indent=2))
                    else:
                        print(run_dir)
                        print(f"arm={arm} fixture={fx} replicate={r}")
                        print(f"prompt={run_dir / 'prompt.md'}")
                        print(f"skill={meta.get('skill')}")
                    return
    raise SystemExit("No awaiting_operator runs left.")


if __name__ == "__main__":
    main()
