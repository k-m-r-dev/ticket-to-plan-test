#!/usr/bin/env python3
"""Emit / ingest blind human (S2) score sheets."""

from __future__ import annotations

import argparse
import json
import secrets
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent


def checklist_for_fixture(fixture: str) -> list[dict]:
    if fixture == "f2":
        data = json.loads((ROOT / "fixtures/todo-api-ambiguous/decision_checklist.json").read_text())
        return data["decisions"]
    data = json.loads((ROOT / "fixtures/todo-api/gold_checklist.json").read_text())
    return data["requirements"]


def emit(protocol: str = "abp-v1") -> None:
    base = BENCH / "runs" / protocol
    sheets_dir = base / "human_sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)
    key = {}
    for meta_path in sorted(base.rglob("meta.json")):
        if "execute" in meta_path.parts or "human_sheets" in meta_path.parts:
            continue
        run_dir = meta_path.parent
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        blind_id = secrets.token_hex(4)
        key[blind_id] = {
            "run_dir": str(run_dir.relative_to(ROOT)),
            "arm": meta["arm"],
            "fixture": meta["fixture"],
            "replicate": meta["replicate"],
        }
        items = checklist_for_fixture(meta["fixture"])
        sheet = {
            "blind_id": blind_id,
            "protocol": protocol,
            "fixture": meta["fixture"],
            "instructions": "Score Yes/No without knowing which arm produced the plan. Do not open mapping_key.json.",
            "items": [{"id": it["id"], "text": it.get("text", ""), "present": None} for it in items],
            "depth_ok": None,
            "guardrails_ok": None,
            "notes": "",
        }
        (sheets_dir / f"{blind_id}.json").write_text(json.dumps(sheet, indent=2) + "\n", encoding="utf-8")
    (sheets_dir / "mapping_key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print(f"emitted {len(key)} sheets -> {sheets_dir}")


def ingest(protocol: str = "abp-v1") -> None:
    base = BENCH / "runs" / protocol
    sheets_dir = base / "human_sheets"
    key = json.loads((sheets_dir / "mapping_key.json").read_text(encoding="utf-8"))
    results = []
    for blind_id, info in key.items():
        sheet_path = sheets_dir / f"{blind_id}.json"
        sheet = json.loads(sheet_path.read_text(encoding="utf-8"))
        answered = [i for i in sheet["items"] if i.get("present") is not None]
        total = len(sheet["items"]) or 1
        ratio = (sum(1 for i in answered if i["present"]) / total) if answered else None
        out = {
            "blind_id": blind_id,
            **info,
            "coverage_ratio": ratio,
            "items_scored": len(answered),
            "items_total": total,
            "depth_ok": sheet.get("depth_ok"),
            "guardrails_ok": sheet.get("guardrails_ok"),
            "complete": len(answered) == total and sheet.get("depth_ok") is not None,
        }
        results.append(out)
        run_dir = ROOT / info["run_dir"]
        s2_path = run_dir / "score_s2.json"
        s2_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    summary = sheets_dir / "s2_summary.json"
    summary.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    complete = sum(1 for r in results if r["complete"])
    print(f"ingested {len(results)} sheets ({complete} complete) -> {summary}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["emit", "ingest"])
    ap.add_argument("--protocol", default="abp-v1")
    args = ap.parse_args()
    if args.command == "emit":
        emit(args.protocol)
    else:
        ingest(args.protocol)


if __name__ == "__main__":
    main()
