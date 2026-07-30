# Notes on v1 baseline runs

These four runs (`bench-todo-*-r1`) were produced during plan implementation in a single agent session (not four separate operator Cursor chats).

- **GSD:** real `gsd_plan_milestone` + `gsd_plan_slice` MCP calls; Delivery & Guardrails appended to ROADMAP
- **OpenSpec:** real `npx openspec new change`; proposal/specs/design/tasks authored
- **no-tools / native:** markdown authored under run `artifacts/`
- **wall_clock_seconds / tokens:** instrumented estimates for harness validation (`tokens.source=estimate_chars`); re-run with operator-filled meta for production comparisons

Re-run protocol: see [README.md](README.md).
