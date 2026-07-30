---
name: abp-matrix-runner
description: >-
  Run one ABP abp-v1 planning matrix slot from the operator runbook. Use when the
  user asks to run the ABP matrix, next benchmark run, abp-matrix-runner, or
  automate OPERATOR_RUNBOOK planning steps. Does plan-only work for a single
  awaiting_operator run; never fills human S2 sheets; never implements the app.
---

# ABP Matrix Runner (one run per invocation)

Automate **one** Acceptance Benchmark Protocol planning slot.  
Human S2 scoring and app implementation are **out of scope**.

## Hard rules

1. Do **exactly one** run per chat/invocation (isolation).
2. **Plan only** — do not implement the Todo API.
3. For `fixture=f2`: do **not** read `fixtures/todo-api-ambiguous/ANSWER_KEY.md`.
4. Do **not** open or edit `benchmark/runs/abp-v1/human_sheets/` (S2 is human-only).
5. Do **not** change [`docs/benchmark/PROTOCOL.md`](../../docs/benchmark/PROTOCOL.md) thresholds.
6. Write plan files only under this run’s `artifacts/` directory (also OK to create OpenSpec/GSD artifacts in-repo, then **copy** finals into `artifacts/`).

## Steps (run in order)

### 1. Pick the next slot

```bash
python3 benchmark/next_run.py --json
```

If exit code nonzero (“No awaiting_operator runs left”), stop and tell the user the matrix planning phase is complete; suggest `validate_runs.py` + human S2.

### 2. Mark start

```bash
python3 benchmark/mark_run.py <run_dir> start --model "<current-model-name>"
```

### 3. Read the prompt only

Read `<run_dir>/prompt.md` and follow its arm instructions.

| arm | How to plan |
| --- | --- |
| `gsd` | Follow `skills/ticket-to-plan-gsd/SKILL.md` + GSD MCP. Scope fully specified for f1 — skip grilling; say so. For f2, grilling is allowed. |
| `openspec` | Follow `skills/ticket-to-plan-openspec/SKILL.md` + OpenSpec. Same ambiguity rule as above. |
| `no-tools` | Follow `skills/ticket-to-plan-no-tools/SKILL.md`; write markdown under this run’s `artifacts/`. |
| `native` | No ticket-to-plan skill. Produce a complete implementation plan markdown in `artifacts/`. |

Stop at plan-ready. Present a one-paragraph design summary; for matrix automation, treat user pre-approval as given for **planning artifacts only** (still no code).

### 4. Ensure artifacts are in the run folder

Copy or write final plan markdown into `<run_dir>/artifacts/` so scoring does not depend on chat history.

### 5. Mark finish + auto-score

Count major tool/MCP/CLI calls used in this run as `--tool-calls N`.

Run these in order — `score.py` copies token counts out of `meta.json`, so `tiktoken_count.py` must populate them first.

```bash
python3 benchmark/mark_run.py <run_dir> finish --tool-calls N --model "<current-model-name>"
python3 benchmark/tiktoken_count.py <run_dir>
python3 benchmark/score.py <run_dir>
```

### 6. Report to the user

Print:

- `run_dir`
- arm / fixture / replicate
- `status=plan_ready`
- S1 coverage/depth from `score.json` if present
- Reminder: start a **new chat** and invoke this skill again for the next run
- Reminder: do not do S2 in this skill

## After all 24 are plan_ready

Tell the user to follow Step 2–3 in [`docs/benchmark/OPERATOR_RUNBOOK.md`](../../docs/benchmark/OPERATOR_RUNBOOK.md) (validate + human sheets). Do not auto-fill S2.
