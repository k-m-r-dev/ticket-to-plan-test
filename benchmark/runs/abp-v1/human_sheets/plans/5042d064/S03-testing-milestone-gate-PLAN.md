# S03 — Integration tests + milestone gate

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — single commit after M001 fully verified
- **Task Handoff Gate** — wait for `do next`
- **Remote Mutation Rule** — no push/PR without approval

## Goal

Achieve full SPEC integration coverage using Axum `TestClient` / tower in-process HTTP tests; clippy clean; ready for human-approved milestone commit.

## Tasks

### T01 — Test harness and app factory

- **Inputs:** Completed router + db pool setup
- **Outputs:** `tests/integration.rs` or `#[cfg(test)]` module with shared `TestClient` and per-test isolated SQLite (temp file or `:memory:`)
- **Validation gate:** `cargo test` — smoke test passes
- **DoD:** No cross-test DB pollution

### T02 — CRUD and filter integration suite

- **Inputs:** SPEC required scenarios
- **Outputs:** Integration tests covering:
  - create → list → get → patch → delete happy path
  - list filter `completed=true` and `completed=false`
  - validation: empty title, title > 200 chars, empty PATCH body, invalid `completed` query param
  - 404 on GET / PATCH / DELETE for unknown UUID
- **Validation gate:** `cargo test` all green

### T03 — Health endpoint test

- **Inputs:** `GET /health`
- **Outputs:** Test asserting `200` and `{ "status": "ok" }`
- **Validation gate:** `cargo test`

### T04 — Clippy and milestone validation

- **Inputs:** Complete codebase
- **Outputs:** Clippy-clean project; optional README with env vars and curl examples
- **Validation gate:** `cargo clippy -- -D warnings`; `cargo test`
- **DoD:** Milestone ready for **human approval before execution commit** (`feat(todo-http-api): implement todo http api`)

## Stop

Human approval required before any implementation or remote mutation. Benchmark planning session ends here.
