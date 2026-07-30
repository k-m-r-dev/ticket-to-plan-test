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

## 1. Project scaffold

- [ ] 1.1 Init Rust binary crate (`Cargo.toml`, `src/main.rs`) with dependencies: `axum`, `tokio` (full features), `sqlx` (sqlite, runtime-tokio, macros features), `serde`/`serde_json`, `uuid` (v4, serde), `chrono` (serde), `tower`, `dotenvy` (optional, for local `.env`).
  - Input: `design.md` Decisions (crate layout, dependency choices)
  - Output: compiling empty crate with `cargo build`
  - Validation gate: `cargo build` succeeds
- [ ] 1.2 Add `sqlx` migration for the `todos` table (`id TEXT PRIMARY KEY`, `title TEXT NOT NULL`, `completed INTEGER NOT NULL DEFAULT 0`, `created_at TEXT NOT NULL`, `updated_at TEXT NOT NULL`) under `migrations/`.
  - Input: `specs/todo-api/spec.md` — Requirement: SQLite persistence
  - Output: `migrations/0001_create_todos.sql`
  - Validation gate: migration applies cleanly via `sqlx::migrate!` against a fresh SQLite file (covered by task 6.1 startup test)
- [ ] 1.3 Add config loading for `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`).
  - Input: `specs/todo-api/spec.md` — Requirement: Server configuration and health check
  - Output: `src/config.rs` with a `Config::from_env()` returning parsed values
  - Validation gate: unit test confirms defaults apply when env vars are unset

## 2. Data model and error types

- [ ] 2.1 Define `Todo` struct (`id: Uuid`, `title: String`, `completed: bool`, `created_at: DateTime<Utc>`, `updated_at: DateTime<Utc>`) with `Serialize`/`Deserialize`/`sqlx::FromRow`.
  - Input: fixture Data model table
  - Output: `src/models.rs`
  - Validation gate: `cargo build`; struct round-trips through `serde_json`
- [ ] 2.2 Define request DTOs: `CreateTodoRequest { title: String, completed: Option<bool> }`, `UpdateTodoRequest { title: Option<String>, completed: Option<bool> }`, and `ListQuery { completed: Option<String> }` (raw string so invalid values can be rejected explicitly).
  - Input: fixture Endpoints section
  - Output: `src/models.rs`
  - Validation gate: `cargo build`
- [ ] 2.3 Implement `AppError` enum (`Validation(String)`, `NotFound`, `Internal`) implementing `IntoResponse`, mapping to `{validation_error: 400, not_found: 404, internal_error: 500}` with the `{ "error": { "code", "message" } }` body shape.
  - Input: `specs/todo-api/spec.md` — Requirement: Standard error shape
  - Output: `src/error.rs`
  - Validation gate: unit test asserts each variant serializes to the exact expected JSON shape and status code

## 3. Validation logic

- [ ] 3.1 Implement title validation (trim; reject empty/whitespace-only; reject length > 200) shared by create and update paths.
  - Input: `specs/todo-api/spec.md` — Requirements: Create a todo, Update a todo
  - Output: `validate_title()` in `src/models.rs` or `src/validation.rs`
  - Validation gate: unit tests for empty, whitespace-only, exactly-200-char (valid), 201-char (invalid) titles
- [ ] 3.2 Implement `completed` query parsing that accepts only exact `"true"`/`"false"` strings and errors otherwise.
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `parse_completed_query()` helper
  - Validation gate: unit tests for `"true"`, `"false"`, missing, and invalid values
- [ ] 3.3 Implement empty-PATCH-body rejection (at least one of `title`/`completed` must be present).
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: check in the PATCH handler or a small validation helper
  - Validation gate: covered by integration test in task 6.4

## 4. Persistence layer

- [ ] 4.1 Implement `SqlitePool` setup and `sqlx::migrate!` run at startup before the listener binds.
  - Input: `design.md` — Decisions (Persistence)
  - Output: `src/db.rs` with `init_pool(database_url: &str) -> SqlitePool`
  - Validation gate: covered by integration test in task 6.1 (fresh DB startup)
- [ ] 4.2 Implement repository functions: `create_todo`, `list_todos(filter: Option<bool>)`, `get_todo(id)`, `update_todo(id, patch)`, `delete_todo(id)` against the `todos` table.
  - Input: `specs/todo-api/spec.md` — all CRUD requirements
  - Output: `src/db.rs` or `src/repository.rs`
  - Validation gate: exercised end-to-end by integration tests in section 6

## 5. HTTP handlers and routing

- [ ] 5.1 Implement `POST /todos` handler: validate title, default `completed=false`, generate `id`/`created_at`/`updated_at`, persist, return `201`.
  - Input: `specs/todo-api/spec.md` — Requirement: Create a todo
  - Output: `src/handlers.rs::create_todo`
  - Validation gate: integration test (task 6.1)
- [ ] 5.2 Implement `GET /todos` handler with optional `completed` filter, returning `200` with a JSON array (empty array allowed).
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `src/handlers.rs::list_todos`
  - Validation gate: integration test (task 6.2)
- [ ] 5.3 Implement `GET /todos/:id` handler returning `200`/Todo or `404`/`not_found`.
  - Input: `specs/todo-api/spec.md` — Requirement: Get a single todo
  - Output: `src/handlers.rs::get_todo`
  - Validation gate: integration test (task 6.3)
- [ ] 5.4 Implement `PATCH /todos/:id` handler applying partial updates, refreshing `updated_at`, returning `200`/updated Todo or `400`/`404` as specified.
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: `src/handlers.rs::update_todo`
  - Validation gate: integration test (task 6.4)
- [ ] 5.5 Implement `DELETE /todos/:id` handler returning `204` empty body or `404`/`not_found`.
  - Input: `specs/todo-api/spec.md` — Requirement: Delete a todo
  - Output: `src/handlers.rs::delete_todo`
  - Validation gate: integration test (task 6.5)
- [ ] 5.6 Implement `GET /health` handler returning `200` `{ "status": "ok" }`, and assemble the full `axum::Router` wiring all routes plus shared `SqlitePool` state.
  - Input: `specs/todo-api/spec.md` — Requirement: Server configuration and health check
  - Output: `src/routes.rs`, `src/main.rs` (binds `HOST:PORT`, applies migrations, serves router)
  - Validation gate: integration test (task 6.6); manual `curl http://127.0.0.1:8080/health` returns expected body

## 6. Integration tests

- [ ] 6.1 Test: create todo — success (`201` + shape), empty/whitespace title (`400`), overlong title (`400`).
  - Input: `specs/todo-api/spec.md` — Requirement: Create a todo
  - Output: `tests/create_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.2 Test: list todos — no filter, `completed=true`, `completed=false`, invalid `completed` value (`400`), empty-list case.
  - Input: `specs/todo-api/spec.md` — Requirement: List todos with optional completion filter
  - Output: `tests/list_todos.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.3 Test: get todo — success, `404` for missing id.
  - Input: `specs/todo-api/spec.md` — Requirement: Get a single todo
  - Output: `tests/get_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.4 Test: patch todo — partial update success, empty body (`400`), invalid title (`400`), `404` for missing id.
  - Input: `specs/todo-api/spec.md` — Requirement: Update a todo
  - Output: `tests/patch_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.5 Test: delete todo — success (`204`, then subsequent `GET` returns `404`), `404` for missing id.
  - Input: `specs/todo-api/spec.md` — Requirement: Delete a todo
  - Output: `tests/delete_todo.rs`
  - Validation gate: `cargo test` passes
- [ ] 6.6 Test: health check and startup migration behavior against a fresh temp SQLite file.
  - Input: `specs/todo-api/spec.md` — Requirements: SQLite persistence, Server configuration and health check
  - Output: `tests/health_and_startup.rs`
  - Validation gate: `cargo test` passes

## 7. Final verification

- [ ] 7.1 Run full validation suite: `cargo test` and `cargo clippy -- -D warnings`; fix any failures/warnings.
  - Input: all prior tasks
  - Output: clean `cargo test` and `cargo clippy -- -D warnings` runs
  - Validation gate: both commands exit 0
- [ ] 7.2 Single milestone commit per Commit Cadence above (`feat(todo-http-api): implement Axum + SQLite CRUD todo API`), only after 7.1 passes and explicit user approval for any push/PR.
  - Input: `design.md` — Delivery & Guardrails
  - Output: one commit containing the full implementation
  - Validation gate: `git status` clean after commit; no push without explicit approval
