# S03 — Integration tests + polish

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — single commit after M001 fully verified
- **Task Handoff Gate** — wait for `do next`
- **Remote Mutation Rule** — no push/PR without approval

## Goal

Full integration coverage using Axum `TestClient` / tower service tests; clippy clean; ready for human-approved milestone commit.

## Tasks

### T01 — Integration test harness

- **Inputs:** Axum app factory (router + in-memory or temp-file SQLite)
- **Outputs:** `tests/` or `#[cfg(test)]` module with shared `TestClient` setup
- **Validation gate:** `cargo test` — at least one smoke test passes
- **DoD:** Each test uses isolated DB (temp file or `:memory:`) to avoid cross-test pollution

### T02 — CRUD + filter integration suite

- **Inputs:** Assumed required scenarios from ticket goals
- **Outputs:** Tests covering:
  - create → list → get → patch → delete happy path
  - list filter `completed=true` / `completed=false`
  - validation: empty title, title > 200, empty PATCH body, invalid `completed` query
  - 404 on get / patch / delete for unknown UUID
- **Validation gate:** `cargo test` all green

### T03 — Health + config smoke

- **Inputs:** `/health` endpoint
- **Outputs:** Test asserting `200` and `{ "status": "ok" }`
- **Validation gate:** `cargo test`

### T04 — Clippy + final milestone gate

- **Inputs:** Complete codebase
- **Outputs:** Clippy-clean project; README with env vars and curl examples (optional)
- **Validation gate:** `cargo clippy -- -D warnings`; `cargo test`
- **DoD:** Milestone ready for **human approval before implementation commit** (`feat(todo-http-api): implement todo http api`)

## Stop

Human approval required before any implementation or remote mutation. Benchmark planning session ends here.
