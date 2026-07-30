# Implementation plan — Todo HTTP API (native arm, ABP f1, r3)

**Source:** Locked benchmark fixture (`fixtures/todo-api`). Planning only — **do not implement** in the benchmark session.

## Architecture overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Axum HTTP  │────▶│  TodoService │────▶│  TodoRepository │
│  routes     │     │  (validation)│     │  (sqlx SQLite)  │
└─────────────┘     └──────────────┘     └─────────────────┘
        │                    │
        └────────────────────┴──▶ AppError → JSON { error: { code, message } }
```

| Layer | Choice |
| --- | --- |
| Language / runtime | Rust + Tokio |
| HTTP | Axum |
| Persistence | SQLite via sqlx |
| Serialization | serde + serde_json |
| IDs | `uuid` crate (server-generated UUID strings) |
| Timestamps | RFC 3339 UTC (`chrono` or `time`) |
| Project root | `apps/todo-api/` |

**Module layout:**

```
apps/todo-api/
  Cargo.toml
  migrations/001_create_todos.sql
  src/
    main.rs          # entry: config, db pool, migrate, bind server
    lib.rs           # create_app(pool) for tests
    config.rs        # HOST, PORT, DATABASE_URL
    db.rs            # pool init, sqlx::migrate! on startup
    models.rs        # Todo struct, request DTOs
    repository.rs    # CRUD queries
    service.rs       # title trim/validation, timestamp updates
    error.rs         # AppError → JSON envelope
    routes/
      mod.rs
      health.rs      # GET /health
      todos.rs       # CRUD + filter handlers
  tests/
    integration.rs   # axum/tower in-process HTTP tests
```

## Data model

`Todo` (JSON + DB row):

| Field | Type | Notes |
| --- | --- | --- |
| `id` | UUID string | Server-generated on create |
| `title` | string | Required; trimmed; length 1..=200 |
| `completed` | boolean | Default `false` on create |
| `created_at` | RFC 3339 UTC | Server-set on create |
| `updated_at` | RFC 3339 UTC | Server-set; updated on every successful PATCH |

**SQLite schema (migration `001_create_todos.sql`):**

```sql
CREATE TABLE todos (
    id          TEXT PRIMARY KEY NOT NULL,
    title       TEXT NOT NULL,
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
```

## Configuration

Environment variables (read at startup):

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:todos.db` | sqlx SQLite connection string |
| `HOST` | `127.0.0.1` | Bind address |
| `PORT` | `8080` | Listen port |

## Error envelope

All 4xx/5xx JSON responses:

```json
{ "error": { "code": "string_snake_case", "message": "human readable" } }
```

Required codes (minimum):

| Code | When |
| --- | --- |
| `validation_error` | Empty/whitespace title, title > 200, empty PATCH body, invalid `completed` query |
| `not_found` | Missing todo id on GET/PATCH/DELETE |
| `internal_error` | Unexpected DB or handler failure (no stack trace in body) |

---

## Phase A — Foundation

### Step 1 — Implement Cargo scaffold

Create `apps/todo-api` with dependencies: `axum`, `tokio` (full), `sqlx` (features: `runtime-tokio`, `sqlite`, `migrate`), `serde`, `serde_json`, `uuid` (v4), `chrono` (or `time`), `tower`, `thiserror`. Add `src/main.rs` and `src/lib.rs` exporting `create_app(pool) -> Router`. **Validation:** `cargo check`.

### Step 2 — Implement configuration module

Add `config.rs` reading `DATABASE_URL`, `HOST`, `PORT` from env with defaults above. Parse `PORT` as `u16`; fail fast on invalid values at startup. **Validation:** unit test that defaults apply when env vars are unset.

### Step 3 — Implement sqlx pool + migrations on startup

Add `db.rs`: create `SqlitePool` from `DATABASE_URL`, run `sqlx::migrate!()` before serving. Migration creates `todos` table per schema. Concurrent-safe enough for single-process local use (sqlx connection pool). **Validation:** start app against temp file; confirm table exists via `SELECT`.

### Step 4 — Implement Todo model and repository

`models.rs`: `Todo` struct with serde for JSON. `CreateTodoRequest`, `UpdateTodoRequest` (PATCH body). `repository.rs`: `create`, `list` (optional `completed` filter), `get_by_id`, `update` (partial), `delete`. On create: generate UUID `id`, set `completed` default false, set `created_at`/`updated_at` to now (UTC RFC 3339). On successful PATCH: refresh `updated_at`. **Validation:** repository integration test against temp DB.

### Step 5 — Implement service layer with validation

`service.rs`: `validate_title(title) -> Result<String, AppError>` — trim whitespace, reject empty, reject length > 200. `validate_patch_body` — require at least one of `title` or `completed`. `parse_completed_filter(query) -> Result<Option<bool>, AppError>` — accept only `true`/`false` strings. **Validation:** unit tests for edge cases (empty, whitespace, 201 chars).

### Step 6 — Implement error helpers

`error.rs`: `AppError` enum mapping to HTTP status and JSON envelope with codes `validation_error`, `not_found`, `internal_error`. Implement `IntoResponse` for Axum. **Validation:** unit test asserting JSON shape.

---

## Phase B — HTTP surface

### Step 7 — Implement GET /health

Route: `GET /health` → `200` `{ "status": "ok" }`. Wire into router in `create_app()`. **Validation:** in-process GET returns expected JSON.

### Step 8 — Implement POST /todos

- Body: `{ "title": string, "completed"?: boolean }`
- Success: `201` with full Todo JSON
- Empty/whitespace-only title or title longer than 200 → `400` `validation_error`
- Trim title before length check and storage

### Step 9 — Implement GET /todos (list + completed filter)

- Optional query: `completed=true` or `completed=false`
- Success: `200` JSON array (empty array allowed)
- Invalid `completed` value (e.g. `completed=maybe`) → `400` `validation_error`
- Natural DB order (no pagination or custom sorting)

### Step 10 — Implement GET /todos/:id

- Success: `200` with Todo
- Missing id → `404` `not_found`

### Step 11 — Implement PATCH /todos/:id

- Body: any subset of `{ "title"?: string, "completed"?: boolean }`
- At least one field required; empty body `{}` → `400` `validation_error`
- Title rules same as create when `title` present
- Success: `200` with updated Todo
- Missing id → `404` `not_found`

### Step 12 — Implement DELETE /todos/:id

- Success: `204` empty body
- Missing id → `404` `not_found`

### Step 13 — Implement server bind

`main.rs`: load config, init pool + migrations, build router via `create_app`, bind `HOST:PORT`, serve with Tokio. **Validation:** manual curl smoke against running server.

---

## Phase C — Verification

### Step 14 — Implement integration test harness

Shared test helper in `tests/integration.rs`: `setup_app()` creates temp `DATABASE_URL`, runs migrations, returns `TestClient` (axum-test or tower `ServiceExt`). **Validation:** `cargo test` smoke passes.

### Step 15 — Implement full integration test suite

Cover all scenarios in `TEST_PLAN.md`: CRUD happy path, list filter, validation failures, 404 paths, health, error envelope shape. **Validation:** `cargo test`.

### Step 16 — Implement clippy gate

Run `cargo clippy -- -D warnings` and fix warnings. **Validation:** clippy clean + `cargo test` green.

## Delivery validation commands

When implementing (out of scope for this planning run):

```bash
cd apps/todo-api
cargo test
cargo clippy -- -D warnings
```

## Out of scope (do not implement)

Authentication / authorization, multi-user tenancy, pagination, sorting beyond natural DB order, soft deletes, web UI / mobile client, OpenAPI generation as required work, Docker / Kubernetes deployment, rate limiting, CORS policy beyond local curl needs, GraphQL / gRPC.
