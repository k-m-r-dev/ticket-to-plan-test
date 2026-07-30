# S03 — Integration tests and milestone polish

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — single commit after full M001 verification
- **Task Handoff Gate** — wait for `do next`
- **Remote Mutation Rule** — no push/PR without approval
- **Human approval** — stop before implementation commit; benchmark planning ends here

## Goal

End-to-end integration coverage, clippy clean, milestone ready for human-approved `feat(todo-http-api): ...` commit.

## Tasks

### T01 — Test harness (Axum TestClient)

- **Inputs:** App factory building router + isolated SQLite (temp file per test)
- **Outputs:** Shared test setup module; `axum::test` or tower `ServiceExt` client
- **Validation gate:** `cargo test` smoke passes
- **DoD:** Tests do not share DB state across cases

### T02 — CRUD integration suite

- **Inputs:** Assumed API contract from ROADMAP
- **Outputs:** Integration tests covering:
  - create → list → get → patch (title + completed) → delete happy path
  - `GET /todos?completed=true` and `?completed=false` after mixed creates
  - validation: empty title POST, overlong title, empty PATCH body, bad `completed` query
  - 404 on get / patch / delete for random UUID
- **Validation gate:** `cargo test` all green

### T03 — Persistence + health integration

- **Inputs:** SQLite file persistence requirement
- **Outputs:** Test that data written in one app instance survives re-init with same `DATABASE_URL`; `/health` returns 200 + `{ "status": "ok" }`
- **Validation gate:** `cargo test`

### T04 — Clippy + milestone gate

- **Inputs:** Complete codebase
- **Outputs:** Clippy-clean project; optional README with env vars and curl examples
- **Validation gate:** `cargo clippy -- -D warnings`; `cargo test`
- **DoD:** Milestone complete; **human approval required before execution** and before any remote mutation

## Stop

Planning-only benchmark run complete. Do not implement until operator approves and issues `do next` per Task Handoff Gate.
