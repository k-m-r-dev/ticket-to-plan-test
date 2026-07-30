#!/usr/bin/env python3
"""ABP comparison report: means/ranges across replicates."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent


def load_rows(protocol: str) -> list[dict]:
    base = BENCH / "runs" / protocol
    rows = []
    if not base.is_dir():
        return rows
    for score_path in sorted(base.rglob("score.json")):
        if "execute" in score_path.parts:
            continue
        run_dir = score_path.parent
        meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
        score = json.loads(score_path.read_text(encoding="utf-8"))
        s2 = {}
        s2p = run_dir / "score_s2.json"
        if s2p.is_file():
            s2 = json.loads(s2p.read_text(encoding="utf-8"))
        s3p = run_dir / "score_s3.json"
        s3 = json.loads(s3p.read_text(encoding="utf-8")) if s3p.is_file() else {}
        tok = (meta.get("tokens") or {}).get("tiktoken") or {}
        rows.append(
            {
                "fixture": meta.get("fixture"),
                "arm": meta.get("arm"),
                "replicate": meta.get("replicate"),
                "status": meta.get("status"),
                "s1_coverage": (score.get("requirement_coverage") or {}).get("ratio"),
                "s1_depth": (score.get("plan_depth") or {}).get("ratio"),
                "s2_coverage": s2.get("coverage_ratio"),
                "s3_faithfulness": s3.get("faithfulness"),
                "wall": meta.get("wall_clock_seconds"),
                "tiktoken": tok.get("total"),
                "tool_calls": meta.get("tool_calls"),
            }
        )
    return rows


def summarize(rows: list[dict], field: str) -> str:
    vals = [r[field] for r in rows if isinstance(r.get(field), (int, float))]
    if not vals:
        return "—"
    if len(vals) == 1:
        return f"{vals[0]:.2f}"
    return f"{statistics.mean(vals):.2f} [{min(vals):.2f}–{max(vals):.2f}]"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    rows = load_rows(args.protocol)
    out = args.out or (BENCH / "runs" / args.protocol / "COMPARISON.md")
    groups: dict[tuple, list] = defaultdict(list)
    for r in rows:
        groups[(r["fixture"], r["arm"])].append(r)

    lines = [
        f"# ABP comparison (`{args.protocol}`)",
        "",
        "| fixture | arm | n | s1_coverage | s1_depth | s2_coverage | s3_faithfulness | wall_s | tiktoken | tools |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for (fixture, arm), rs in sorted(groups.items()):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(fixture),
                    str(arm),
                    str(len(rs)),
                    summarize(rs, "s1_coverage"),
                    summarize(rs, "s1_depth"),
                    summarize(rs, "s2_coverage"),
                    summarize(rs, "s3_faithfulness"),
                    summarize(rs, "wall"),
                    summarize(rs, "tiktoken"),
                    summarize(rs, "tool_calls"),
                ]
            )
            + " |"
        )
    lines.append("")
    awaiting = sum(1 for r in rows if r.get("status") == "awaiting_operator")
    scored = sum(1 for r in rows if r.get("s1_coverage") is not None)
    lines.append(f"Runs with S1 scores: {scored}. Still awaiting_operator (meta): {awaiting}.")
    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
