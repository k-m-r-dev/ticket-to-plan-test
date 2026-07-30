# S03 — Quality gate & integration verification

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — single commit after M001 fully verified
- **Task Handoff Gate** — wait for `do next`
- **Remote Mutation Rule** — no push/PR without approval

## Goal

Prove SPEC compliance with Axum `TestClient` / tower in-process HTTP integration tests; pass clippy; stop for human approval before any implementation commit.

## Tasks

### T01 — Integration test harness

- **Inputs:** App factory (router + pool) from S01/S02
- **Outputs:** `tests/api_integration.rs` (or `#[cfg(test)]` module) with per-test isolated SQLite (`:memory:` or temp file)
- **Validation gate:** `cargo test` — smoke passes
- **DoD:** No cross-test pollution; helper to POST/GET/PATCH/DELETE with JSON assertions

### T02 — CRUD and filter integration suite

- **Inputs:** SPEC required scenarios
- **Outputs:** Integration tests covering:
  - create → list → get → patch → delete happy path
  - list filter `completed=true` and `completed=false`
  - validation: empty title, title > 200 chars, empty PATCH body, invalid `completed` query param
  - 404 on GET / PATCH / DELETE for unknown UUID
- **Validation gate:** `cargo test` all green

### T03 — Health and error-code assertions

- **Inputs:** `/health` and error responses from S02
- **Outputs:** Test `GET /health` → `200` `{ "status": "ok" }`; at least one test per required error code (`validation_error`, `not_found`)
- **Validation gate:** `cargo test`

### T04 — Clippy and milestone stop gate

- **Inputs:** Complete planned codebase
- **Outputs:** Clippy-clean tree; optional README with env vars and curl examples (not required for scoring)
- **Validation gate:** `cargo clippy -- -D warnings`; `cargo test`
- **DoD:** Milestone ready for **human approval before execution** — stop here; no commit until operator says `do next` (`feat(todo-http-api): implement todo http api`)

## Stop

Human approval required before any implementation or remote mutation. Benchmark planning session ends here.
