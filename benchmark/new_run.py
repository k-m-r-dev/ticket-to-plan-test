#!/usr/bin/env python3
"""Scaffold a benchmark run directory for one planning arm."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SPEC = ROOT / "fixtures" / "todo-api" / "SPEC.md"
RUNS = Path(__file__).resolve().parent / "runs"

ARM_SKILL = {
    "gsd": "skills/ticket-to-plan-gsd/SKILL.md",
    "openspec": "skills/ticket-to-plan-openspec/SKILL.md",
    "no-tools": "skills/ticket-to-plan-no-tools/SKILL.md",
    "native": None,
}

ARM_INSTRUCTIONS = {
    "gsd": (
        "Follow skills/ticket-to-plan-gsd/SKILL.md with GSD workflow MCP. "
        "Scope is fully specified — skip grilling. Stop at plan-ready; do not implement."
    ),
    "openspec": (
        "Follow skills/ticket-to-plan-openspec/SKILL.md with OpenSpec (npx openspec / /opsx-*). "
        "Scope is fully specified — skip grilling. Stop at plan-ready; do not implement."
    ),
    "no-tools": (
        "Follow skills/ticket-to-plan-no-tools/SKILL.md. Write plans only under this run's "
        "artifacts/ directory. Scope is fully specified — skip grilling. Do not implement."
    ),
    "native": (
        "No ticket-to-plan skill. Produce a complete implementation plan for the SPEC below. "
        "Write the plan markdown into this run's artifacts/. Do not implement code."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--arm",
        required=True,
        choices=sorted(ARM_SKILL.keys()),
        help="Planning arm to scaffold",
    )
    parser.add_argument("--replicate", type=int, default=1, help="Replicate number (default 1)")
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run id (default: <timestamp>-<arm>-r<n>)",
    )
    args = parser.parse_args()

    if not FIXTURE_SPEC.is_file():
        raise SystemExit(f"Missing fixture spec: {FIXTURE_SPEC}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{ts}-{args.arm}-r{args.replicate}"
    run_dir = RUNS / run_id
    artifacts = run_dir / "artifacts"
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")

    artifacts.mkdir(parents=True)
    spec_text = FIXTURE_SPEC.read_text(encoding="utf-8")
    skill = ARM_SKILL[args.arm]
    prompt = "\n".join(
        [
            f"# Benchmark prompt — arm `{args.arm}`",
            "",
            "## Instructions",
            "",
            ARM_INSTRUCTIONS[args.arm],
            "",
            f"## Skill path",
            "",
            skill or "(none — native planning)",
            "",
            "## Output",
            "",
            f"Copy or write final plan artifacts into `{artifacts.relative_to(ROOT)}/`.",
            "Fill meta.json started_at/ended_at, wall_clock_seconds, tokens, tool_calls when done.",
            "",
            "## Locked SPEC",
            "",
            spec_text,
            "",
        ]
    )
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    shutil.copy2(FIXTURE_SPEC, run_dir / "SPEC.md")

    meta = {
        "run_id": run_id,
        "arm": args.arm,
        "replicate": args.replicate,
        "fixture": "todo-api",
        "skill": skill,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": None,
        "ended_at": None,
        "wall_clock_seconds": None,
        "tokens": {
            "input": None,
            "output": None,
            "total": None,
            "source": "none",
            "notes": "",
        },
        "tool_calls": None,
        "artifact_paths": [],
        "status": "created",
        "notes": "",
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(run_dir)


if __name__ == "__main__":
    main()
