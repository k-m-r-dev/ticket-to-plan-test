# TODO — DeepEval follow-up project

**Status:** Deferred from v1 benchmark (this repo).  
**Upstream:** https://github.com/confident-ai/deepeval  

## Why separate

DeepEval is an LLM evaluation framework (Python). Integrating it here would mix planning-skill benchmarking with a second product dependency and typically needs API keys / Confident AI cloud. Keep capture here; evaluate elsewhere.

## What this repo already produces

Each run under `benchmark/runs/<run_id>/`:

| File | Use for DeepEval |
| --- | --- |
| `prompt.md` | Input / retrieval context (locked SPEC + arm instructions) |
| `artifacts/**` | Model “actual output” (plan markdown) |
| `meta.json` | Latency, best-effort tokens, tool_calls, arm id |
| `score.json` | Heuristic rubric scores (baseline to compare against LLM judges) |
| `fixtures/todo-api/gold_checklist.json` | Expected coverage / out-of-scope themes |

Suggested export: a JSONL line per run:

```json
{
  "input": "<SPEC text>",
  "actual_output": "<concatenated plan artifacts>",
  "expected_output": "<optional gold plan summary>",
  "context": ["fixtures/todo-api/SPEC.md"],
  "metadata": {"arm": "gsd", "run_id": "...", "wall_clock_seconds": 120}
}
```

## Metrics to port later

1. **Faithfulness / hallucination** — plan claims vs SPEC only (maps to our `not_in_scope` penalties).
2. **Answer relevancy / coverage** — checklist item presence with an LLM judge instead of keywords.
3. **Summarization / concision** — penalize over-planning (maps to overplanning_penalty).
4. **Custom GEval** — “Does the plan include testable tasks for every endpoint?”

## Cursor-session limitations

v1 runs are **Cursor agent sessions**, so token counts are best-effort (`tokens.source`: `cursor_ui` | `estimate_chars` | `unknown`). A DeepEval project that needs exact tokens should either:

- Re-run arms via an API harness that injects the same skill text, or
- Accept null tokens and judge quality only.

## Suggested next repo tasks

1. Create sibling project `ticket-to-plan-deepeval` with `deepeval` + pytest.
2. Add `benchmark/export_jsonl.py` here to emit JSONL from scored runs.
3. Implement GEval metrics aligned to `GOLD_RUBRIC.md`.
4. Compare LLM-judge scores vs keyword `score.py` ratios for calibration.
5. Do **not** block this repo’s v1 COMPARISON.md on DeepEval results.

## Non-goals for that follow-up

- Replacing the four Cursor arms
- Auto-implementing the Todo API
- Mutating GSD/OpenSpec during eval
