#!/usr/bin/env python3
"""Emit a comparison table for scored benchmark runs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "runs"


def load_scores(arm_filter: list[str] | None = None) -> list[dict]:
    rows = []
    if not RUNS.is_dir():
        return rows
    for score_path in sorted(RUNS.glob("*/score.json")):
        data = json.loads(score_path.read_text(encoding="utf-8"))
        if arm_filter and data.get("arm") not in arm_filter:
            continue
        meta_path = score_path.parent / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
        tokens = data.get("tokens") or meta.get("tokens") or {}
        gf = data.get("guardrail_fidelity") or {}
        rows.append(
            {
                "run_id": data["run_id"],
                "arm": data["arm"],
                "replicate": meta.get("replicate", 1),
                "wall_clock_s": data.get("wall_clock_seconds"),
                "tokens_total": tokens.get("total"),
                "tool_calls": data.get("tool_calls"),
                "coverage": (data.get("requirement_coverage") or {}).get("ratio"),
                "depth": (data.get("plan_depth") or {}).get("ratio"),
                "guardrails": gf.get("ratio") if gf.get("applicable", True) else "N/A",
                "files": (data.get("artifact_bulk") or {}).get("file_count"),
                "bytes": (data.get("artifact_bulk") or {}).get("bytes"),
                "hallucinations": (data.get("hallucination_penalty") or {}).get("count"),
                "overplan": (data.get("overplanning_penalty") or {}).get("count"),
            }
        )
    return rows


def fmt(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def to_markdown(rows: list[dict]) -> str:
    headers = [
        "arm",
        "run_id",
        "wall_clock_s",
        "tokens_total",
        "tool_calls",
        "coverage",
        "depth",
        "guardrails",
        "files",
        "bytes",
        "hallucinations",
        "overplan",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(h)) for h in headers) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arms", nargs="*", help="Optional arm filter")
    parser.add_argument(
        "--out",
        default=None,
        help="Write markdown report path (default: benchmark/runs/COMPARISON.md)",
    )
    parser.add_argument("--csv", default=None, help="Optional CSV output path")
    args = parser.parse_args()

    rows = load_scores(args.arms)
    if not rows:
        raise SystemExit("No scored runs found under benchmark/runs/*/score.json")

    md = "# Benchmark comparison\n\n" + to_markdown(rows)
    out = Path(args.out) if args.out else RUNS / "COMPARISON.md"
    out.write_text(md, encoding="utf-8")
    print(out)
    print(md)

    if args.csv:
        csv_path = Path(args.csv)
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(csv_path)


if __name__ == "__main__":
    main()
