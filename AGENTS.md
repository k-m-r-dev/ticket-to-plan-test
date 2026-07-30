## Learned User Preferences

- Prefer grilling one decision at a time (with a recommended answer) and brainstorming/design approval before any execution
- When adapting skills for tool swaps, copy the original skill file first, then modify the copy rather than rewriting in place
- For planning-skill benchmarks, prefer a greenfield fixture in-repo over bolting onto an existing app or using a spec-only fixture
- Prefer fixture-first benchmark setup: lock the subject SPEC and gold rubric before forking skills / building the harness / running arms
- Prefer plain-language, step-by-step operator instructions for benchmark runbooks
- Prefer tool/approach-neutral benchmarking aimed at undoubtable, data-driven evidence rather than favoring any planning arm

## Learned Workspace Facts

- This repo is a GSD sandbox used to benchmark ticket-to-plan: GSD-backed vs OpenSpec-backed vs skill-only vs native planning
- Shared benchmark subject: greenfield Rust Todo HTTP API (Axum + SQLite as default stack), with fixtures `f1` (fully locked SPEC) and `f2` (ambiguous ticket; `ANSWER_KEY.md` sealed during planning)
- Acceptance Benchmark Protocol (ABP / abp-v1): 2 fixtures × 4 arms × 3 repeats = 24 plan-only runs; S1 automated rubric + human S2; no execute-to-score
- Human S2 scoring is operator-only via `benchmark/runs/abp-v1/human_sheets/`; agents must not edit those sheets or PROTOCOL thresholds
- Planning automation: `.cursor/skills/abp-matrix-runner/` (one slot per chat) and unattended `benchmark/run_matrix.py`; operator docs in `docs/benchmark/OPERATOR_RUNBOOK.md` and `AGENT_RUNNER.md`
- Metrics capture: Python harness under `benchmark/` (including TikToken); DeepEval remains a deferred TODO for a separate project
- OpenSpec ticket-to-plan variant is a thin adapter: keep ticket-to-plan steps/guardrails, swap GSD MCP/files for OpenSpec artifacts and CLI
- Canonical GitHub remote for this project: `k-m-r-dev/ticket-to-plan-test`
- Team-facing benchmark explanation (plain language + mermaid, pros/cons, slide outline): `docs/benchmark/ticket-to-plan-openspec-benchmark-explained.md`
