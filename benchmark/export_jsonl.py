#!/usr/bin/env python3
"""Export ABP runs to JSONL for DeepEval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent


def concat_artifacts(run_dir: Path) -> str:
    art = run_dir / "artifacts"
    chunks: list[str] = []
    if art.is_dir():
        for f in sorted(art.rglob("*")):
            if f.is_file() and f.suffix.lower() in {".md", ".txt", ".json"}:
                chunks.append(f"<!-- {f.relative_to(run_dir)} -->\n" + f.read_text(encoding="utf-8", errors="replace"))
    return "\n\n".join(chunks)


def iter_abp_runs(protocol: str = "abp-v1"):
    base = BENCH / "runs" / protocol
    if not base.is_dir():
        return
    for meta_path in sorted(base.rglob("meta.json")):
        if "execute" in meta_path.parts:
            continue
        yield meta_path.parent


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    out = args.out or (BENCH / "runs" / args.protocol / "export.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with out.open("w", encoding="utf-8") as fh:
        for run_dir in iter_abp_runs(args.protocol) or []:
            meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
            prompt = (run_dir / "prompt.md").read_text(encoding="utf-8") if (run_dir / "prompt.md").is_file() else ""
            actual = concat_artifacts(run_dir)
            if not actual.strip():
                continue
            row = {
                "input": prompt,
                "actual_output": actual,
                "context": [str(ROOT / "fixtures" / "todo-api" / "SPEC.md")],
                "metadata": {
                    "run_id": meta.get("run_id"),
                    "arm": meta.get("arm"),
                    "fixture": meta.get("fixture"),
                    "replicate": meta.get("replicate"),
                    "protocol": meta.get("protocol"),
                    "status": meta.get("status"),
                },
            }
            fh.write(json.dumps(row) + "\n")
            n += 1
    print(f"wrote {n} lines -> {out}")


if __name__ == "__main__":
    main()
