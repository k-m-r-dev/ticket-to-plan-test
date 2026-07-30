# Design: todo-http-api

## Approach

Single binary Axum app with `sqlx` SQLite pool, migrations at startup, handlers for health + todos CRUD.

## Stack

- Rust, Tokio, Axum
- sqlx (SQLite) + migrations
- serde / serde_json for JSON
- uuid for ids
- chrono or time for RFC 3339 timestamps

## Modules

- `main` / `app` — router, state, bind HOST:PORT
- `db` — pool + migrate
- `error` — AppError → JSON envelope
- `todos` — routes, handlers, queries
- `tests` — in-process HTTP integration tests

## Data flow

Client → Axum route → validate → sqlx query → JSON Todo / error envelope.

## Testing

Tower/`axum::test` style in-process requests against a temp SQLite file covering create, list, filter, get, patch, delete, validation, and 404.
