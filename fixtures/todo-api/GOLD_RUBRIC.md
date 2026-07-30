# Gold Rubric — Todo API Planning Benchmark

Score each plan artifact set against `gold_checklist.json`.

## Scoring rules

1. **Requirement coverage** — fraction of `requirements` items with `present: true` (keyword/semantic match in plan text).
2. **Plan depth** — all `depth` items present for the arm’s expected artifact shape (see arm notes in checklist).
3. **Guardrail fidelity** — fraction of `guardrails` items present when the arm claims ticket-to-plan process (gsd, openspec, no-tools). Native arm: score N/A (excluded from mean) unless plan invents a delivery section — then score normally.
4. **Tool-call burden** — from `meta.json` `tool_calls` (lower is not automatically better; report raw).
5. **Artifact bulk** — total UTF-8 bytes and file count under `artifacts/`.
6. **Hallucination penalty** — count of `not_in_scope` themes the plan treats as required work (auth, UI, pagination as required, etc.).
7. **Over-planning penalty** — count of tasks clearly outside gold scope (e.g. OpenAPI as required milestone, k8s).

## Pass guidance (informational)

A strong plan covers ≥90% requirements, full depth for its arm, zero hallucination hits, and low over-planning.
