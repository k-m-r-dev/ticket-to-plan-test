# Tasks: todo-http-api-abp-f2-r1

## Guardrails (embedded)

- **Task Handoff Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — pause after each task; wait for explicit `do next`
- **Commit Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — commit only after verified scope per commit cadence
- **Remote Mutation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — no push/PR without explicit user approval
- **Validation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — run `cargo test` and `cargo clippy -- -D warnings` before commit/push
- **Commit Message Format** (`skills/ticket-to-plan-openspec/SKILL.md`) — `feat(todo-http-api): summary`
- **Milestone Commit Cadence** (`skills/ticket-to-plan-openspec/SKILL.md`) — do **not** commit per checkbox; one commit after the whole change is verified
- **Full Plan Depth Rule** / **OpenSpec Artifact Completeness Rule** — proposal, specs, design, tasks present; apply only after human approval

Commit cadence: **milestone** (single commit after the whole change is verified).

---

## 1. Scaffold + persistence (S01)

- [ ] 1.1 Create `apps/todo-api` Cargo binary with dependencies: axum, tokio, sqlx (sqlite + migrate), serde/serde_json, uuid, chrono (or time), tracing
  - Inputs: design D1–D2; assumed stack from CLARIFICATIONS
  - Outputs: `Cargo.toml`, `src/main.rs` skeleton
  - Validate: `cargo check` in crate directory

- [ ] 1.2 Add sqlx migration for `todos` table (`id` TEXT PK, `title` TEXT, `completed` INTEGER/BOOL, `created_at`, `updated_at`)
  - Inputs: data model from `specs/todo-api/spec.md`
  - Outputs: `migrations/00x_*.sql`
  - Validate: migrate against a temp DB file without error

- [ ] 1.3 Wire config (`DATABASE_URL` default `sqlite:todos.db`, `HOST`/`PORT` defaults), open pool, run migrations on startup, expose `GET /health` → `200` `{ "status": "ok" }`
  - Inputs: design D8; health requirement
  - Outputs: `config`/`db`/`app` modules; listening server
  - Validate: process starts; health check returns 200

## 2. Todo CRUD + filter + errors (S02)

- [ ] 2.1 Implement shared `AppError` → JSON envelope `{ "error": { "code", "message" } }` with `validation_error`, `not_found`, `internal_error`
  - Inputs: error-shape requirement; design D4
  - Outputs: `error` module + `IntoResponse`
  - Validate: unit or handler test asserts envelope shape

- [ ] 2.2 Implement `POST /todos` (trim title, length 1..=200, optional `completed`, server UUID + timestamps, `201`)
  - Inputs: create + model requirements
  - Outputs: create handler + model serde types
  - Validate: integration test create success; empty/whitespace and overlong title → 400 `validation_error`

- [ ] 2.3 Implement `GET /todos` with optional `completed=true|false` (invalid → 400)
  - Inputs: list/filter requirement; design D5
  - Outputs: list handler
  - Validate: list all + filter true/false + bad query tests; empty DB returns `[]`

- [ ] 2.4 Implement `GET /todos/:id`, `PATCH /todos/:id` (non-empty body, title rules, refresh `updated_at`), `DELETE /todos/:id` (`204`)
  - Inputs: get/patch/delete requirements
  - Outputs: remaining handlers
  - Validate: success paths + 404 for get/patch/delete + empty PATCH → 400

## 3. Integration tests + polish (S03)

- [ ] 3.1 Complete in-process HTTP integration suite: create, list, filter, get, patch, delete; empty/overlong title; empty PATCH; bad `completed` query; 404 get/patch/delete
  - Inputs: integration-test requirement; design D9
  - Outputs: `tests/` or `#[cfg(test)]` module using temp SQLite
  - Validate: `cargo test`

- [ ] 3.2 Clippy clean and final verification
  - Inputs: validation commands from Delivery & Guardrails
  - Outputs: no clippy warnings under `-D warnings`
  - Validate: `cargo clippy -- -D warnings`; then single milestone commit only after human approval to commit

## Stop

Plan-ready. Do **not** run `/opsx-apply` or implement until explicit human approval.
