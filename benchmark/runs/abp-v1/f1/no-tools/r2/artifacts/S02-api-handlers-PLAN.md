# S02 — API handlers (CRUD, filter, validation, errors)

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone**
- **Task Handoff Gate** — wait for `do next`
- **Validation Rule** — handler-level tests where practical

## Goal

Implement all `/todos` endpoints with title validation, `completed` query filter, PATCH body rules, and a consistent JSON error envelope.

## Tasks

### T01 — Todo domain model and repository

- **Inputs:** SPEC fields — `id` (UUID string, server-generated), `title`, `completed`, `created_at`, `updated_at` (RFC 3339 UTC)
- **Outputs:** `Todo` struct with serde; `TodoRepository` with `create`, `list`, `get_by_id`, `update`, `delete` using sqlx pool
- **Validation gate:** Repository smoke test against temp SQLite
- **DoD:** Create sets timestamps; successful PATCH updates `updated_at`

### T02 — POST /todos (create)

- **Inputs:** Body `{ "title": string, "completed"?: boolean }`
- **Outputs:** `201` + full Todo JSON; `400` + `validation_error` for empty/whitespace-only title or title length > 200
- **Validation gate:** Tests — happy path, trimmed title, empty title, overlong title, default `completed=false`
- **DoD:** Title trimmed before persist

### T03 — GET /todos (list + completed filter)

- **Inputs:** Optional query `completed=true` or `completed=false`
- **Outputs:** `200` JSON array (empty allowed); `400` `validation_error` for invalid `completed` value
- **Validation gate:** Tests — unfiltered list, `completed=true`, `completed=false`, bad query param

### T04 — GET /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `200` Todo; `404` `not_found` for missing id
- **Validation gate:** Existing get + 404 test

### T05 — PATCH /todos/:id

- **Inputs:** Body any subset of `{ "title"?: string, "completed"?: boolean }`; at least one field required
- **Outputs:** `200` updated Todo; `400` for empty body or title validation failure; `404` missing id
- **Validation gate:** Patch title, patch completed, empty body 400, 404

### T06 — DELETE /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `204` empty body; `404` `not_found`
- **Validation gate:** Delete success + 404

### T07 — Centralized error responses

- **Inputs:** SPEC error shape — all 4xx/5xx JSON: `{ "error": { "code": "string_snake_case", "message": "human readable" } }`
- **Outputs:** `AppError` enum + `IntoResponse` mapping; codes at minimum: `validation_error`, `not_found`, `internal_error`
- **Validation gate:** Assert error codes in handler tests
- **DoD:** Unexpected failures return `internal_error` without leaking stack traces
