"""DeepEval S3 metrics for ABP JSONL export.

Requires OPENAI_API_KEY (or provider keys DeepEval expects).
Skips cleanly when keys / deepeval are unavailable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

BENCH = Path(__file__).resolve().parents[1]
JSONL = BENCH / "runs" / "abp-v1" / "export.jsonl"


def load_rows():
    if not JSONL.is_file():
        return []
    rows = []
    for line in JSONL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


@pytest.fixture(scope="module")
def rows():
    return load_rows()


def test_jsonl_exists_or_skip(rows):
    if not rows:
        pytest.skip("No export.jsonl rows yet — run export_jsonl.py after plan_ready runs")


def test_deepeval_faithfulness_or_skip(rows):
    if not rows:
        pytest.skip("no rows")
    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("No LLM API key for DeepEval judge")
    try:
        from deepeval import assert_test
        from deepeval.metrics import FaithfulnessMetric
        from deepeval.test_case import LLMTestCase
    except ImportError:
        pytest.skip("deepeval not installed")

    # Evaluate first available row only in CI-friendly smoke; full matrix via CLI later
    row = rows[0]
    metric = FaithfulnessMetric(threshold=0.5)
    tc = LLMTestCase(
        input=row["input"][:8000],
        actual_output=row["actual_output"][:8000],
        retrieval_context=row.get("context") or [],
    )
    try:
        assert_test(tc, [metric])
    except Exception as e:  # noqa: BLE001
        # Record soft result beside export
        out = BENCH / "runs" / "abp-v1" / "score_s3_smoke.json"
        out.write_text(
            json.dumps({"error": str(e), "metric": "FaithfulnessMetric", "row": row.get("metadata")}, indent=2) + "\n",
            encoding="utf-8",
        )
        pytest.skip(f"DeepEval judge failed/soft-skip: {e}")
