# Acceptance Benchmark Protocol (ABP) — abp-v1

**Status:** FROZEN for abp-v1  
**Version:** `abp-v1`  
**Frozen date:** 2026-07-30  
**Stance:** Tool-agnostic method comparison. No preferred backend declared before results.

## Research questions

1. Do four planning methods differ on plan quality for the same product intent?
2. Does a structured skill (with or without GSD/OpenSpec) beat native planning on guardrails and ambiguous inputs?
3. Do plans from each method yield a working API under a locked execute oracle?

## Arms (exact)

| Arm id | Skill / prompt | Backend |
| --- | --- | --- |
| `gsd` | [`skills/ticket-to-plan-gsd/SKILL.md`](../../skills/ticket-to-plan-gsd/SKILL.md) | GSD workflow MCP |
| `openspec` | [`skills/ticket-to-plan-openspec/SKILL.md`](../../skills/ticket-to-plan-openspec/SKILL.md) | OpenSpec CLI / `/opsx-*` |
| `no-tools` | [`skills/ticket-to-plan-no-tools/SKILL.md`](../../skills/ticket-to-plan-no-tools/SKILL.md) | Markdown artifacts only |
| `native` | No skill — SPEC/ticket + “complete implementation plan” | None |

### Skill content hashes (SHA-256)

| Path | sha256 |
| --- | --- |
| `skills/ticket-to-plan-gsd/SKILL.md` | `72839df045754a24bfde7dadc4fd2547ee7c3cd3bbfaa6a70c071806226c6149` |
| `skills/ticket-to-plan-openspec/SKILL.md` | `b4ac4da318061b17f7d0bd67b1abc0ae2a8c605466e98b5724dc0e0af8b9f144` |
| `skills/ticket-to-plan-no-tools/SKILL.md` | `3719ec3a1d89ff4b3fff9a4d11127e7a512966e1cdf507c5d92c7149eab2fd87` |

Changing any skill text requires protocol version bump + full re-run.

## Fixtures

| Id | Path | Role |
| --- | --- | --- |
| `f1` | [`fixtures/todo-api/`](../../fixtures/todo-api/) | Locked Todo HTTP API SPEC |
| `f2` | [`fixtures/todo-api-ambiguous/`](../../fixtures/todo-api-ambiguous/) | Ambiguous ticket + answer key |

### Fixture hashes (SHA-256)

| Path | sha256 |
| --- | --- |
| `fixtures/todo-api/SPEC.md` | `df90965d2390ab6d5bc96a0f16057ca0db35fc2be0053d163d1ad99a6a15ac16` |
| `fixtures/todo-api/gold_checklist.json` | `d6efb7272b901b85aeffae6178cec84f87388def963398287a5ffbcfe84d9f87` |
| `fixtures/todo-api-ambiguous/TICKET.md` | `e6e1ecf556a3420f4baae07429ab3040a31f5f50c9017595edbc24ee21735a89` |
| `fixtures/todo-api-ambiguous/ANSWER_KEY.md` | `a55e4ed06ec85ec7e65cc5e95e6e4552a76ac9f05f41fa8ab33f3611883244c0` |
| `fixtures/todo-api-ambiguous/decision_checklist.json` | `58a0218dca6a3d84a0a2b68675486f3c962f87cd1d7d6b592fbf5bbef6aa3ae1` |
| `fixtures/todo-api/oracle/test_contract.py` | `330ac8fb5a3c294d43b0c8d09895c0fb344887efa7303b66cf74bf362b8ffb4a` |

Also see `fixtures/todo-api-ambiguous/HASHES.md`.

## Design

- Replicates: **n = 3** per arm per fixture  
- Matrix: **4 arms × 2 fixtures × 3 = 24** planning runs  
- Stop rule: plan-ready only; **no implementation** during planning runs  
- Isolation: one Cursor chat per run; no cross-arm artifact leakage  
- Run root: `benchmark/runs/abp-v1/<fixture>/<arm>/r<n>/`

## Scoring layers

| Layer | Name | Primary? |
| --- | --- | --- |
| **S1** | Automated rubric (`benchmark/score.py`) | Supporting |
| **S2** | Blind human gold checklist | **Primary for acceptance claims** |
| **S3** | DeepEval / GEval (`benchmark/acceptance/`) | Supporting |

If S1 and S2 disagree, publish the disagreement; do not silently prefer S1.

## Cost signals (all recorded; none claimed as Cursor billing)

1. Wall-clock from real `started_at` / `ended_at`  
2. `tool_calls` count  
3. TikToken on prompt + artifacts (record encoding name)  
4. Optional Cursor UI usage paste (`tokens.cursor_ui`)  
5. Artifact file count and bytes  

## Execute-to-score

- Scope: **F1 only**, **one plan per arm** (median S2 coverage among that arm’s 3 replicates)  
- Oracle: [`fixtures/todo-api/oracle/`](../../fixtures/todo-api/oracle/) — locked from SPEC only **before** plan selection  
- Budget: one agent implementation session per selected plan (document deviations)  
- Record under `benchmark/runs/abp-v1/execute/<arm>/`

## Pre-registered decision rules (do not edit post-hoc)

**R1 — F1 method parity (gsd vs openspec):**  
Mean S2 coverage and mean S2 depth for `gsd` and `openspec` differ by **≤ 0.05** (5 percentage points).

**R2 — F1 guardrails vs native:**  
Mean S2 guardrail fidelity for `gsd`, `openspec`, and `no-tools` each **exceed** mean S2 guardrails for `native` (native may be N/A → treat native guardrails as 0.0 for this rule).

**R3 — F2 ambiguity:**  
Mean S2 “answer-key decision correctness” for each ticket-to-plan arm (`gsd`, `openspec`, `no-tools`) **exceeds** `native`.

**R4 — Execute disclosure:**  
Report oracle pass rate for each of the four F1 implements. No rule requires a winner; **failing to run or hiding a rate fails acceptance**.

**Acceptance pass:** R1 ∧ R2 ∧ R3 ∧ R4 documented in `ACCEPTANCE_REPORT.md`.  
If any rule fails, report FAIL with data — that is still a valid scientific outcome.

## Protocol change rule

Any change to fixtures, skills, checklists, thresholds, or scoring definitions requires a **new protocol version** and full re-run of the matrix.

## Operator

See [`OPERATOR_RUNBOOK.md`](OPERATOR_RUNBOOK.md).
