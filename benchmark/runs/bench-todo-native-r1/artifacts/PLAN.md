# Implementation plan — Todo HTTP API (native)

Build a Rust HTTP Todo API with Axum, Tokio, and SQLite via sqlx. No UI.

## Steps

1. Create a Cargo binary crate; add axum, tokio, sqlx (sqlite), serde, uuid, chrono.
2. Add sqlx migration for `todos` (`id`, `title`, `completed`, `created_at`, `updated_at`); migrate on startup.
3. Configure `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (`127.0.0.1`), `PORT` (`8080`).
4. Implement `GET /health` → `200` `{ "status": "ok" }`.
5. Implement `POST /todos` (201; title 1..=200; optional `completed`).
6. Implement `GET /todos` with optional `completed` query filter (invalid → 400).
7. Implement `GET /todos/:id`, `PATCH /todos/:id`, `DELETE /todos/:id` (404 when missing; DELETE 204).
8. Standardize JSON errors: `{ "error": { "code": "...", "message": "..." } }` with `validation_error`, `not_found`, `internal_error`.
9. Write integration tests for CRUD, filter, validation, and 404 paths.
10. Run `cargo test` and `cargo clippy -- -D warnings`.

## Out of scope

Auth, web UI, pagination, Docker/K8s, GraphQL.

## Test plan

In-process HTTP tests against a temporary SQLite database covering each endpoint and failure mode above.
