#!/usr/bin/env python3
"""Scaffold an ABP (or legacy) benchmark run directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = Path(__file__).resolve().parent
RUNS = BENCH / "runs"

ARM_SKILL = {
    "gsd": "skills/ticket-to-plan-gsd/SKILL.md",
    "openspec": "skills/ticket-to-plan-openspec/SKILL.md",
    "no-tools": "skills/ticket-to-plan-no-tools/SKILL.md",
    "native": None,
}

FIXTURES = {
    "f1": {
        "id": "todo-api",
        "input": ROOT / "fixtures" / "todo-api" / "SPEC.md",
        "label": "Locked SPEC",
    },
    "f2": {
        "id": "todo-api-ambiguous",
        "input": ROOT / "fixtures" / "todo-api-ambiguous" / "TICKET.md",
        "label": "Ambiguous ticket",
    },
}

ARM_INSTRUCTIONS = {
    "gsd": "Follow skills/ticket-to-plan-gsd/SKILL.md with GSD MCP. Stop at plan-ready; do not implement.",
    "openspec": "Follow skills/ticket-to-plan-openspec/SKILL.md with OpenSpec. Stop at plan-ready; do not implement.",
    "no-tools": "Follow skills/ticket-to-plan-no-tools/SKILL.md. Write plans only under this run's artifacts/. Do not implement.",
    "native": "No ticket-to-plan skill. Produce a complete implementation plan. Write into artifacts/. Do not implement.",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--arm", required=True, choices=sorted(ARM_SKILL))
    p.add_argument("--fixture", choices=sorted(FIXTURES), default="f1")
    p.add_argument("--replicate", type=int, default=1)
    p.add_argument("--protocol", default="abp-v1", help="Use 'legacy' for old flat runs/")
    p.add_argument("--run-id", default=None)
    args = p.parse_args()

    fx = FIXTURES[args.fixture]
    if not fx["input"].is_file():
        raise SystemExit(f"Missing fixture input: {fx['input']}")

    skill = ARM_SKILL[args.arm]
    skill_hash = sha256_file(ROOT / skill) if skill else None
    fixture_hash = sha256_file(fx["input"])

    if args.protocol == "legacy":
        run_id = args.run_id or f"legacy-{args.arm}-r{args.replicate}"
        run_dir = RUNS / run_id
    else:
        run_id = args.run_id or f"{args.protocol}-{args.fixture}-{args.arm}-r{args.replicate}"
        run_dir = RUNS / args.protocol / args.fixture / args.arm / f"r{args.replicate}"

    artifacts = run_dir / "artifacts"
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")
    artifacts.mkdir(parents=True)

    body = fx["input"].read_text(encoding="utf-8")
    prompt = "\n".join(
        [
            f"# Benchmark prompt — protocol `{args.protocol}` arm `{args.arm}` fixture `{args.fixture}` r{args.replicate}",
            "",
            "## Instructions",
            "",
            ARM_INSTRUCTIONS[args.arm],
            "",
            f"## Skill",
            "",
            skill or "(none — native)",
            "",
            f"## Fixture ({fx['label']})",
            "",
            body,
            "",
            "## Output",
            "",
            f"Write plan artifacts into `{artifacts.relative_to(ROOT)}/`.",
            "Fill meta.json started_at/ended_at, tool_calls, tokens when done.",
            "",
        ]
    )
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    shutil.copy2(fx["input"], run_dir / "input.md")

    meta = {
        "protocol": args.protocol,
        "run_id": run_id,
        "arm": args.arm,
        "fixture": args.fixture,
        "fixture_id": fx["id"],
        "replicate": args.replicate,
        "skill": skill,
        "skill_hash": skill_hash,
        "fixture_hash": fixture_hash,
        "model": None,
        "transcript_ref": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": None,
        "ended_at": None,
        "wall_clock_seconds": None,
        "tokens": {
            "tiktoken": {"total": None, "encoding": None},
            "cursor_ui": {"total": None, "notes": ""},
            "estimate_chars": {"total": None},
        },
        "tool_calls": None,
        "artifact_paths": [],
        "status": "awaiting_operator",
        "notes": "",
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(run_dir)


if __name__ == "__main__":
    main()
