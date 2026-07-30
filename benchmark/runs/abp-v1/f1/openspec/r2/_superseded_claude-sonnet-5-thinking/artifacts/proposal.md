## Why

We need a local Todo HTTP API backed by SQLite so that a single-process client can create, read, update, delete, and filter todos over JSON/HTTP without any UI. The scope is fully specified by the locked benchmark fixture (`fixtures/todo-api/SPEC.md`) — no product ambiguity remains, so this proposal skips grilling and goes straight to planning.

## What Changes

- Add a new Axum-based HTTP server exposing `POST /todos`, `GET /todos` (with `completed` filter), `GET /todos/:id`, `PATCH /todos/:id`, `DELETE /todos/:id`, and `GET /health`.
- Add SQLite persistence via `sqlx`, with schema applied through migrations on startup, configurable via `DATABASE_URL` (default `sqlite:todos.db`).
- Add server-side validation for title (required, trimmed, 1..=200 chars), `completed` query parsing, and non-empty PATCH bodies, all returning the standard `{ "error": { "code", "message" } }` shape on failure.
- Add integration tests covering create, list, list-with-filter, get, patch, delete, and all specified validation/404 error paths.
- Add configuration for `HOST` (default `127.0.0.1`) and `PORT` (default `8080`).

## Capabilities

### New Capabilities
- `todo-api`: CRUD + completion-filter HTTP API for todos, including validation rules, error shape, persistence, and server startup/health behavior.

### Modified Capabilities
- None — this is a greenfield capability; no existing specs are being changed.

## Impact

- **New code**: Rust/Axum service crate (routes, handlers, SQLite repository layer, migrations, error types, config loading).
- **New dependencies**: `axum`, `tokio`, `sqlx` (sqlite feature), `serde`/`serde_json`, `uuid`, `chrono` (or `time`) for RFC 3339 timestamps, `tower`/`axum::test` helpers for integration tests.
- **New data store**: local SQLite file (`todos.db` by default) — no shared/multi-instance requirement.
- **No impact** on authentication, multi-tenancy, pagination, soft deletes, UI, OpenAPI generation, deployment tooling, or rate limiting/CORS beyond Axum defaults — all explicitly out of scope per the locked fixture.
