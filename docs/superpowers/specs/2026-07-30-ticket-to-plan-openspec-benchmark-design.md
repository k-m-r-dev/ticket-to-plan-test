# ticket-to-plan vs OpenSpec Benchmark Design

**Date:** 2026-07-30  
**Status:** Approved (grill + brainstorm lock)

## Goal

Compare four ways of producing an implementation plan from the same locked spec:

1. Original `ticket-to-plan` with GSD workflow MCP
2. Modified `ticket-to-plan` with OpenSpec (thin adapter)
3. `ticket-to-plan` process without GSD or OpenSpec
4. Native AI planning (no ticket-to-plan skill)

Measure wall-clock, best-effort tokens, and rubric accuracy (plus agreed secondary metrics).

## Locked decisions

| Decision | Choice |
| --- | --- |
| Subject | Greenfield Rust HTTP Todo API (Axum + SQLite/sqlx), no UI |
| Input | Fully locked `fixtures/todo-api/SPEC.md` (skip grilling) |
| Accuracy | Rubric-only vs gold checklist (no execute-to-score in v1) |
| Harness | Python under `benchmark/`; Cursor agent sessions; best-effort tokens |
| OpenSpec skill | Thin adapter (same steps, OpenSpec backend) |
| Replicates | n=1 now; schema supports `replicate` for n≥3 |
| Approach | Fixture-first |
| DeepEval | Deferred (`benchmark/TODO_deepeval.md`) |

## Metrics

- Wall-clock (prompt start → plan-ready)
- Tokens (best-effort / nullable)
- Requirement coverage (% of gold checklist present)
- Plan depth completeness (workstream→unit→slice→task or OpenSpec proposal/specs/design/tasks)
- Guardrail fidelity (delivery/guardrail citations where applicable)
- Tool-call burden (MCP/CLI/tool invocations)
- Artifact bulk (markdown bytes / file count)
- Hallucinated constraints (penalty: invents requirements not in SPEC)
- Over-planning (penalty: tasks beyond gold scope)

## Fixture

- `fixtures/todo-api/SPEC.md` — locked API contract
- `fixtures/todo-api/GOLD_RUBRIC.md` + `gold_checklist.json` — scorable items + not-in-scope list

No Todo API implementation during v1 benchmark runs.

## Skills

| Path | Role |
| --- | --- |
| `skills/ticket-to-plan-gsd/SKILL.md` | Preserved GSD-dependent skill |
| `skills/ticket-to-plan-openspec/SKILL.md` | Thin adapter to OpenSpec artifacts |
| `skills/ticket-to-plan-no-tools/SKILL.md` | Same process; hand-authored markdown only |
| (none) | Arm 4 native prompt |

`skills/MAPPING.md` documents GSD ↔ OpenSpec term mapping.

OpenSpec is installed alongside `.gsd/` (not a replacement).

## Harness

```text
benchmark/
  schema/run_record.schema.json
  new_run.py / score.py / report.py
  runs/<run_id>/{meta.json,prompt.md,artifacts/,score.json}
  TODO_deepeval.md
```

## Arms

| Arm id | Skill | Backend |
| --- | --- | --- |
| `gsd` | ticket-to-plan-gsd | GSD MCP |
| `openspec` | ticket-to-plan-openspec | OpenSpec CLI / `/opsx:*` |
| `no-tools` | ticket-to-plan-no-tools | Markdown under run artifacts |
| `native` | — | SPEC + “complete implementation plan” |

## Out of scope (v1)

- Implementing the Todo API from any arm’s plan
- Automated Cursor token APIs
- DeepEval package integration
- Removing GSD from this repo

## Self-review

- No TBD placeholders for locked decisions
- Fixture and scoring agree on out-of-scope → hallucination penalties
- Arms differ only by planning method; input SPEC is constant
