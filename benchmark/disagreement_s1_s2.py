#!/usr/bin/env python3
"""Publish S1 vs S2 disagreement report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    args = ap.parse_args()
    base = BENCH / "runs" / args.protocol
    lines = [
        f"# S1 vs S2 disagreement (`{args.protocol}`)",
        "",
        "| run | arm | fixture | s1_coverage | s2_coverage | delta |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    n = 0
    for s1p in sorted(base.rglob("score.json")):
        if "execute" in s1p.parts:
            continue
        run_dir = s1p.parent
        s2p = run_dir / "score_s2.json"
        if not s2p.is_file():
            continue
        meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
        s1 = json.loads(s1p.read_text(encoding="utf-8"))
        s2 = json.loads(s2p.read_text(encoding="utf-8"))
        a = (s1.get("requirement_coverage") or {}).get("ratio")
        b = s2.get("coverage_ratio")
        if a is None or b is None:
            continue
        delta = b - a
        lines.append(
            f"| {meta.get('run_id')} | {meta.get('arm')} | {meta.get('fixture')} | {a:.2f} | {b:.2f} | {delta:+.2f} |"
        )
        n += 1
    if n == 0:
        lines.append("")
        lines.append("_No paired S1/S2 scores yet. Complete operator runs and `human_sheet.py ingest`._")
    out = base / "DISAGREEMENT_S1_S2.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
