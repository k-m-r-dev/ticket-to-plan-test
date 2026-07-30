## Learned User Preferences

- Prefer grilling one decision at a time (with a recommended answer) and brainstorming/design approval before any execution
- When adapting skills for tool swaps, copy the original skill file first, then modify the copy rather than rewriting in place
- For planning-skill benchmarks, prefer a greenfield fixture in-repo over bolting onto an existing app or using a spec-only fixture

## Learned Workspace Facts

- This repo is a GSD sandbox used to benchmark ticket-to-plan: GSD-backed vs OpenSpec-backed vs skill-only vs native planning
- Shared benchmark subject: greenfield Rust Todo HTTP API (Axum + SQLite as default stack), fully locked requirements doc as the fixture
- Accuracy for v1 is rubric-only against a gold checklist; no execute-to-score
- Metrics capture: Python harness under `benchmark/`; all four arms run as Cursor agent sessions (best-effort tokens); DeepEval is a deferred TODO for a separate project
- OpenSpec ticket-to-plan variant is a thin adapter: keep ticket-to-plan steps/guardrails, swap GSD MCP/files for OpenSpec artifacts and CLI
