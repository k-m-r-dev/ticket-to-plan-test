# Implementation plan — Local Todo HTTP API (native arm, f2 r3)

**Source:** Ambiguous benchmark ticket. Assumed decisions in `DESIGN_SUMMARY.md`.  
**Scope:** Planning only — do **not** implement during the benchmark session.

## Technology choices

| Concern | Decision |
| --- | --- |
| Language | Rust |
| HTTP framework | Axum |
| Async runtime | Tokio |
| Database | SQLite via sqlx |
| Serialization | serde + serde_json |
| IDs | uuid crate (server-generated string UUIDs) |
| Timestamps | RFC 3339 UTC (chrono or time) |
| Location | `apps/todo-api/` |

## Directory layout

```
apps/todo-api/
  Cargo.toml
  migrations/001_create_todos.sql
  src/
    main.rs           # startup: config, pool, migrate, serve
    lib.rs            # create_app() for tests
    config.rs         # DATABASE_URL, HOST, PORT
    db.rs             # pool + sqlx::migrate! on startup
    models.rs         # Todo struct, repository functions
    error.rs          # AppError → JSON envelope
    routes/
      mod.rs
      health.rs       # GET /health
      todos.rs        # CRUD + filter handlers
  tests/
    integration.rs    # in-process HTTP tests
```

## Data model

### Todo (JSON + DB)

| Field | Type | Rules |
| --- | --- | --- |
| `id` | string (UUID) | Server-generated on create |
| `title` | string | Required; trimmed; length 1..=200 |
| `completed` | boolean | Default `false` on create |
| `created_at` | RFC 3339 UTC | Set on create |
| `updated_at` | RFC 3339 UTC | Updated on every successful PATCH |

### SQLite migration `001_create_todos.sql`

```sql
CREATE TABLE todos (
  id TEXT PRIMARY KEY NOT NULL,
  title TEXT NOT NULL,
  completed INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## Configuration

| Env var | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:todos.db` | sqlx connection string |
| `HOST` | `127.0.0.1` | Bind address |
| `PORT` | `8080` | Listen port |

Fail fast at startup if `PORT` is not a valid `u16`.

## API contract

### GET /health

- Response: `200` `{ "status": "ok" }`

### POST /todos

- Body: `{ "title": string, "completed"?: boolean }`
- Success: `201` full Todo JSON
- Empty/whitespace title or title > 200 chars → `400` `validation_error`

### GET /todos

- Optional query: `completed=true` or `completed=false`
- Success: `200` JSON array (may be empty)
- Invalid `completed` value → `400` `validation_error`
- Natural DB order; no pagination

### GET /todos/:id

- Success: `200` Todo JSON
- Unknown id → `404` `not_found`

### PATCH /todos/:id

- Body: subset of `{ "title"?: string, "completed"?: boolean }`; at least one field required
- Empty body `{}` → `400` `validation_error`
- Title rules same as create when `title` present
- Success: `200` updated Todo
- Unknown id → `404` `not_found`

### DELETE /todos/:id

- Success: `204` empty body
- Unknown id → `404` `not_found`

## Error envelope

All 4xx/5xx responses:

```json
{ "error": { "code": "validation_error", "message": "human readable detail" } }
```

| Code | When |
| --- | --- |
| `validation_error` | Bad input (title, empty PATCH, invalid query) |
| `not_found` | Todo id does not exist |
| `internal_error` | Unexpected DB/handler failure (no stack in body) |

## Implementation steps

### Step 1 — Cargo scaffold

Create `apps/todo-api` with dependencies: `axum`, `tokio`, `sqlx` (`runtime-tokio`, `sqlite`), `serde`, `serde_json`, `uuid`, `chrono`, `tower`. Stub `main.rs` and `lib.rs` with empty `create_app() -> Router`. **Validation:** `cargo check`.

### Step 2 — Configuration module

Implement `config.rs` loading `DATABASE_URL`, `HOST`, `PORT` with defaults. **Validation:** unit test defaults; reject invalid `PORT`.

### Step 3 — Database pool and migrations

Implement `db.rs`: connect pool, run `sqlx::migrate!()` before serving. **Validation:** start against temp file; confirm `todos` table exists; data survives restart.

### Step 4 — Model and repository

`models.rs`: `Todo` struct with serde. Repository: `create`, `list` (optional `completed` filter), `get_by_id`, `update` (partial), `delete`. Trim title; set timestamps on create/update. **Validation:** repository unit tests or integration smoke.

### Step 5 — Error mapping

`error.rs`: map domain errors to JSON envelope; implement Axum `IntoResponse`. **Validation:** unit test JSON shape for `validation_error` and `not_found`.

### Step 6 — Health route

Wire `GET /health` → `200` `{ "status": "ok" }`. **Validation:** curl or in-process GET.

### Step 7 — POST /todos

Implement create handler with title validation (trim, 1..=200). **Validation:** integration test create → `201`.

### Step 8 — GET /todos with completed filter

List all or filter by `completed` query param. **Validation:** integration tests for filter true/false and invalid query.

### Step 9 — GET /todos/:id

Single-todo fetch. **Validation:** integration test `200` and `404`.

### Step 10 — PATCH /todos/:id

Partial update; reject empty body; refresh `updated_at`. **Validation:** integration tests for completion toggle and validation failures.

### Step 11 — DELETE /todos/:id

Hard delete. **Validation:** integration test `204` then `GET` → `404`.

### Step 12 — Server entrypoint

`main.rs`: load config, init pool + migrations, bind `HOST:PORT`, serve. **Validation:** manual curl smoke.

### Step 13 — Integration test harness

Shared `setup_app()` with isolated temp `DATABASE_URL` per test; use `axum_test::TestClient` or tower `ServiceExt`. **Validation:** `cargo test` smoke passes.

### Step 14 — Full integration suite

Implement scenarios in `TEST_PLAN.md` (CRUD, filter, validation, 404, health, error envelope). **Validation:** `cargo test`.

### Step 15 — Quality gate

Run `cargo clippy -- -D warnings`; fix warnings. **Validation:** clippy clean + all tests green.

## Delivery validation (when implementing, out of scope here)

```bash
cd apps/todo-api
cargo test
cargo clippy -- -D warnings
```

## Out of scope (do not implement)

Authentication, multi-tenant design, pagination, sorting controls, soft deletes, web/mobile UI, OpenAPI as required work, Docker/Kubernetes, rate limiting, CORS policy beyond local needs, GraphQL/gRPC.
