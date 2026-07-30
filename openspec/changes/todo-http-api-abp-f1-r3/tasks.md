## Guardrails & Commit Cadence (summary — full detail in `design.md`)

**Commit cadence: `milestone`** — one commit only, after the entire change below is implemented and verified. Apply agents must not commit per checkbox.

- **Task Handoff Gate** — pause after each task; wait for explicit `do next`
- **Commit Gate** — commit only after verified scope per `milestone` cadence
- **Remote Mutation Rule** — no push/PR without explicit user approval
- **Validation Rule** — run `cargo test` and `cargo clippy -- -D warnings` before commit/push
- **Commit Message Format** — `feat(todo-http-api): summary`
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`)
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`)
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`)
- **OpenSpec Artifact Completeness Rule**
- **Full Plan Depth Rule**
- **Milestone Commit Cadence**
- **Plan-Doc Embed Rule**

## 1. Expand skeleton crate

- [ ] 1.1 Update `apps/todo-api/Cargo.toml` with dependencies: `axum`, `tokio` (full features), `sqlx` (sqlite, runtime-tokio, macros), `serde`/`serde_json`, `uuid` (v4, serde), `chrono` (serde), `tower`, `tower-http` (trace, optional), `thiserror`.
  - Input: `design.md` Decisions (crate location, dependency choices)
  - Output: compiling `Cargo.toml`
  - Validation gate: `cd apps/todo-api && cargo build` succeeds
- [ ] 1.2 Add `sqlx` migration for the `todos` table (`id TEXT PRIMARY KEY`, `title TEXT NOT NULL`, `completed INTEGER NOT NULL DEFAULT 0`, `created_at TEXT NOT NULL`, `updated_at TEXT NOT NULL`) under `apps/todo-api/migrations/`.
  - Input: `specs/todo-api/spec.md` — Requirement: SQLite persistence
  - Output: `migrations/0001_create_todos.sql`
  - Validation gate: migration applies via `sqlx::migrate!` against fresh SQLite (covered by task 6.6)
- [ ] 1.3 Implement `src/config.rs` loading `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`).
  - Input: `specs/todo-api/spec.md` — Requirement: Server configuration and health check
  - Output: `Config::from_env()` with unit test for defaults
  - Validation gate: unit test passes when env vars unset

## 2. Data model and error types

- [ ] 2.1 Define `Todo` struct with `Serialize`/`Deserialize`/`sqlx::FromRow` and request DTOs (`CreateTodoRequest`, `UpdateTodoRequest`, `ListQuery`).
  - Input: fixture Data model and Endpoints sections
  - Output: `src/models.rs`
  - Validation gate: `cargo build`; serde round-trip test
- [ ] 2.2 Implement `AppError` enum implementing `IntoResponse` mapping to `{validation_error: 400, not_found: 404, internal_error: 500}` with standard error JSON shape.
  - Input: `specs/todo-api/spec.md` — Requirement: Standard error shape
  - Output: `src/error.rs`
  - Validation gate: unit tests assert status codes and JSON body for each variant

## 3. Validation logic

- [ ] 3.1 Implement title validation (trim; reject empty/whitespace-only; reject length > 200) shared by create and update.
  - Input: `specs/todo-api/spec.md` — Requirements: Create a todo, Update a todo
  - Output: `validate_title()` in `src/models.rs`
  - Validation gate: unit tests for empty, whitespace-only, 200-char valid, 201-char invalid
- [ ] 3.2 Implement `completed` query parsing accepting only exact `"true"`/`"false"`.
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `parse_completed_query()` helper
  - Validation gate: unit tests for valid, missing, and invalid values
- [ ] 3.3 Implement empty-PATCH-body rejection (at least one of `title`/`completed` required).
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: validation in PATCH handler
  - Validation gate: integration test in task 6.4

## 4. Persistence layer

- [ ] 4.1 Implement `init_pool(database_url)` running `sqlx::migrate!` before returning `SqlitePool`.
  - Input: `design.md` — Decisions (Persistence)
  - Output: `src/db.rs`
  - Validation gate: integration test 6.6 (fresh DB startup)
- [ ] 4.2 Implement repository functions: `create_todo`, `list_todos`, `get_todo`, `update_todo`, `delete_todo`.
  - Input: `specs/todo-api/spec.md` — all CRUD requirements
  - Output: `src/db.rs`
  - Validation gate: exercised by integration tests in section 6

## 5. HTTP handlers and routing

- [ ] 5.1 Implement `POST /todos`: validate title, default `completed=false`, generate id/timestamps, persist, return `201`.
  - Input: `specs/todo-api/spec.md` — Requirement: Create a todo
  - Output: `src/handlers/todos.rs::create_todo`
  - Validation gate: integration test 6.1
- [ ] 5.2 Implement `GET /todos` with optional `completed` filter, returning `200` JSON array.
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `src/handlers/todos.rs::list_todos`
  - Validation gate: integration test 6.2
- [ ] 5.3 Implement `GET /todos/:id` returning `200`/Todo or `404`/`not_found`.
  - Input: `specs/todo-api/spec.md` — Requirement: Get a single todo
  - Output: `src/handlers/todos.rs::get_todo`
  - Validation gate: integration test 6.3
- [ ] 5.4 Implement `PATCH /todos/:id` with partial updates, refreshing `updated_at`.
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: `src/handlers/todos.rs::update_todo`
  - Validation gate: integration test 6.4
- [ ] 5.5 Implement `DELETE /todos/:id` returning `204` or `404`.
  - Input: `specs/todo-api/spec.md` — Requirement: Delete a todo
  - Output: `src/handlers/todos.rs::delete_todo`
  - Validation gate: integration test 6.5
- [ ] 5.6 Implement `GET /health` and assemble `Router` in `src/app.rs`; wire startup in `src/main.rs` binding `HOST:PORT`.
  - Input: `specs/todo-api/spec.md` — Requirement: Server configuration and health check
  - Output: `src/handlers/health.rs`, `src/app.rs`, updated `src/main.rs`
  - Validation gate: integration test 6.6

## 6. Integration tests

- [ ] 6.1 Test create: success (`201`), empty/whitespace title (`400`), overlong title (`400`).
  - Input: `specs/todo-api/spec.md` — Requirement: Create a todo
  - Output: `tests/create_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.2 Test list: no filter, `completed=true`, `completed=false`, invalid query (`400`), empty list.
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `tests/list_todos.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.3 Test get: success, `404` for missing id.
  - Input: `specs/todo-api/spec.md` — Requirement: Get a single todo
  - Output: `tests/get_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.4 Test patch: partial update, empty body (`400`), invalid title (`400`), `404`.
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: `tests/patch_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.5 Test delete: success (`204`, subsequent get `404`), `404` for missing id.
  - Input: `specs/todo-api/spec.md` — Requirement: Delete a todo
  - Output: `tests/delete_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.6 Test health check and startup migration against fresh SQLite.
  - Input: `specs/todo-api/spec.md` — Requirements: SQLite persistence, Server configuration
  - Output: `tests/health_and_startup.rs`
  - Validation gate: `cargo test` passes

## 7. Final verification

- [ ] 7.1 Run `cd apps/todo-api && cargo test && cargo clippy -- -D warnings`; fix failures.
  - Input: all prior tasks
  - Output: clean test and clippy runs
  - Validation gate: both commands exit 0
- [ ] 7.2 Single milestone commit (`feat(todo-http-api): implement Axum + SQLite CRUD todo API`) after 7.1 passes; no push without explicit approval.
  - Input: `design.md` — Delivery & Guardrails
  - Output: one commit with full implementation
  - Validation gate: `git status` clean; no push without approval
