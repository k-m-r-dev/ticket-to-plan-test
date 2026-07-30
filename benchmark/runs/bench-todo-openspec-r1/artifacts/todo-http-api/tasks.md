# Tasks: todo-http-api

## Guardrails (embedded)

- **Task Handoff Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — pause after each task; wait for `do next`
- **Commit Gate** — commit only after verified change (milestone cadence)
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo test`; `cargo clippy -- -D warnings`
- **Milestone Commit Cadence** — do not commit per checkbox; one commit after change verification

Commit cadence: **milestone** (single commit after the whole change is verified).

## S01 — Scaffold + persistence

- [ ] T01 Create Cargo project with axum, tokio, sqlx (sqlite), serde, uuid, chrono
  - Validate: `cargo check`
- [ ] T02 Add sqlx migrations for `todos` table (id, title, completed, created_at, updated_at)
  - Validate: migrate on startup against temp DB
- [ ] T03 Wire `DATABASE_URL`, `HOST`, `PORT` + `GET /health`
  - Validate: server starts; `/health` → 200

## S02 — Todo CRUD + filter + validation

- [ ] T04 Implement `POST /todos` with title validation (1..=200) and 201
  - Validate: integration test create + empty title 400
- [ ] T05 Implement `GET /todos` + `completed` filter (+ invalid → 400)
  - Validate: list + filter tests
- [ ] T06 Implement `GET|PATCH|DELETE /todos/:id` (404/204/validation)
  - Validate: get/patch/delete + 404 tests
- [ ] T07 Shared error JSON (`validation_error`, `not_found`, `internal_error`)
  - Validate: assert error envelope in tests

## S03 — Tests + polish

- [ ] T08 Complete integration suite for CRUD, validation, 404
  - Validate: `cargo test`
- [ ] T09 Clippy clean
  - Validate: `cargo clippy -- -D warnings`

## Stop

Human approval required before `/opsx-apply` / implementation.
