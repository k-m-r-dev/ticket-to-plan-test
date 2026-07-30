#!/usr/bin/env python3
"""Count TikToken tokens on prompt + artifacts; update meta.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ENCODING = "cl100k_base"


def gather_text(run_dir: Path) -> str:
    parts: list[str] = []
    for name in ("prompt.md", "input.md"):
        p = run_dir / name
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
    art = run_dir / "artifacts"
    if art.is_dir():
        for f in sorted(art.rglob("*")):
            if f.is_file() and f.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"}:
                parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dir", type=Path, help="Path to a run directory with meta.json")
    ap.add_argument("--encoding", default=ENCODING)
    args = ap.parse_args()
    run_dir = args.run_dir
    meta_path = run_dir / "meta.json"
    if not meta_path.is_file():
        raise SystemExit(f"Missing {meta_path}")

    text = gather_text(run_dir)
    est = max(0, len(text) // 4)
    try:
        import tiktoken

        enc = tiktoken.get_encoding(args.encoding)
        total = len(enc.encode(text))
        encoding = args.encoding
    except Exception as e:  # noqa: BLE001
        total = est
        encoding = f"fallback_chars/4 ({e.__class__.__name__})"

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    tokens = meta.setdefault("tokens", {})
    tokens["tiktoken"] = {"total": total, "encoding": encoding}
    tokens["estimate_chars"] = {"total": est}
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), "tiktoken": total, "encoding": encoding, "estimate_chars": est}))


if __name__ == "__main__":
    main()
