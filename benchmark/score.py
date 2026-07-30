#!/usr/bin/env python3
"""Score a benchmark run's artifacts against fixtures/todo-api/gold_checklist.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "fixtures" / "todo-api" / "gold_checklist.json"
RUNS = Path(__file__).resolve().parent / "runs"


def strip_exclusion_sections(text: str) -> str:
    """Remove Non-goals / Out of scope sections so exclusion lists are not penalized."""
    pattern = re.compile(
        r"(?im)^(#{1,6}\s*)?(non-goals|out of scope|out-of-scope)\b.*?(?=^#{1,6}\s+\S|\Z)",
        re.DOTALL,
    )
    return pattern.sub("", text)


def load_artifacts_text(artifacts_dir: Path) -> tuple[str, int, int]:
    texts: list[str] = []
    file_count = 0
    total_bytes = 0
    if not artifacts_dir.is_dir():
        return "", 0, 0
    for path in sorted(artifacts_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"}:
            data = path.read_bytes()
            total_bytes += len(data)
            file_count += 1
            texts.append(data.decode("utf-8", errors="replace"))
    return "\n".join(texts), file_count, total_bytes


def item_present(text: str, item: dict) -> bool:
    lower = text.lower()
    keywords = item.get("keywords") or []
    hits = sum(1 for kw in keywords if kw.lower() in lower)
    if not keywords:
        return item.get("text", "").lower() in lower
    # Require at least half of keywords (ceil), minimum 1
    need = max(1, (len(keywords) + 1) // 2)
    return hits >= need


def score_list(text: str, items: list[dict]) -> dict:
    results = []
    present = 0
    for item in items:
        ok = item_present(text, item)
        if ok:
            present += 1
        results.append({"id": item["id"], "present": ok, "text": item.get("text", "")})
    total = len(items) or 1
    return {
        "items": results,
        "present_count": present,
        "total": len(items),
        "ratio": present / total if items else None,
    }


def hallucination_hits(text: str, items: list[dict]) -> dict:
    """Penalty if out-of-scope themes appear as required work."""
    lower = text.lower()
    hits = []
    for item in items:
        keywords = item.get("keywords") or []
        # Stronger bar for penalties: need 2+ keyword hits or a clear "must/shall" nearby
        kw_hits = [kw for kw in keywords if kw.lower() in lower]
        if len(kw_hits) >= 2:
            hits.append({"id": item["id"], "matched": kw_hits, "text": item.get("text", "")})
        elif len(kw_hits) == 1:
            # Look for requirement-like language near the keyword
            kw = kw_hits[0].lower()
            for m in re.finditer(re.escape(kw), lower):
                window = lower[max(0, m.start() - 40) : m.end() + 40]
                if any(w in window for w in ("must", "shall", "required", "implement", "add auth")):
                    hits.append({"id": item["id"], "matched": kw_hits, "text": item.get("text", "")})
                    break
    return {"hits": hits, "count": len(hits)}


def overplanning_penalty(text: str) -> dict:
    patterns = [
        (r"openapi\s+(as\s+)?required", "openapi_required"),
        (r"kubernetes", "kubernetes"),
        (r"dockerfile", "dockerfile"),
        (r"graphql\s+api", "graphql"),
        (r"react\s+(app|ui|frontend)", "react_ui"),
    ]
    lower = text.lower()
    hits = []
    for pat, name in patterns:
        if re.search(pat, lower):
            hits.append(name)
    return {"hits": hits, "count": len(hits)}


def resolve_run_dir(run_id: str) -> Path:
    direct = RUNS / run_id
    if (direct / "meta.json").is_file():
        return direct
    matches = list(RUNS.rglob(run_id))
    for m in matches:
        if (m / "meta.json").is_file():
            return m
    # path-like argument
    cand = Path(run_id)
    if (cand / "meta.json").is_file():
        return cand
    raise SystemExit(f"Cannot resolve run: {run_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id", help="Run id or path under benchmark/runs/")
    args = parser.parse_args()

    run_dir = resolve_run_dir(args.run_id)
    meta_path = run_dir / "meta.json"
    if not meta_path.is_file():
        raise SystemExit(f"Missing meta.json in {run_dir}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    arm = meta["arm"]
    fixture = meta.get("fixture", "f1")
    if fixture == "f2":
        gold_path = ROOT / "fixtures" / "todo-api-ambiguous" / "decision_checklist.json"
        gold_raw = json.loads(gold_path.read_text(encoding="utf-8"))
        gold = {
            "requirements": gold_raw.get("decisions", []),
            "depth": gold_raw.get("depth", {}),
            "guardrails": gold_raw.get("guardrails", []),
            "not_in_scope": [],
        }
    else:
        gold = json.loads(GOLD.read_text(encoding="utf-8"))
    text, file_count, total_bytes = load_artifacts_text(run_dir / "artifacts")
    penalty_text = strip_exclusion_sections(text)

    requirements = score_list(text, gold["requirements"])
    depth_items = gold["depth"].get(arm, gold["depth"].get("native", []))
    depth = score_list(text, depth_items)
    guardrails = score_list(text, gold["guardrails"])
    if arm == "native":
        guardrail_score = {
            "applicable": False,
            "ratio": None,
            "note": "Native arm: guardrails N/A unless plan includes delivery section",
            **guardrails,
        }
    else:
        guardrail_score = {"applicable": True, **guardrails}

    hall = hallucination_hits(penalty_text, gold["not_in_scope"])
    over = overplanning_penalty(penalty_text)

    score = {
        "run_id": args.run_id,
        "arm": arm,
        "requirement_coverage": requirements,
        "plan_depth": depth,
        "guardrail_fidelity": guardrail_score,
        "artifact_bulk": {"file_count": file_count, "bytes": total_bytes},
        "hallucination_penalty": hall,
        "overplanning_penalty": over,
        "wall_clock_seconds": meta.get("wall_clock_seconds"),
        "tokens": meta.get("tokens"),
        "tool_calls": meta.get("tool_calls"),
    }

    out = run_dir / "score.json"
    out.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    meta["status"] = "scored"
    meta["artifact_paths"] = [
        str(p.relative_to(run_dir))
        for p in sorted((run_dir / "artifacts").rglob("*"))
        if p.is_file()
    ]
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(out)
    print(
        f"coverage={requirements['ratio']:.2f} depth={depth['ratio']:.2f} "
        f"hallucinations={hall['count']} overplan={over['count']} files={file_count}"
    )


if __name__ == "__main__":
    main()
