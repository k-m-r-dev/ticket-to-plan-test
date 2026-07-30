# S02 — Todo CRUD, filter, validation, errors

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone**
- **Task Handoff Gate** — wait for `do next` after each task
- **Validation Rule** — handler/repository tests per endpoint where practical

## Goal

Implement full `/todos` REST surface, `completed` query filter, title validation, PATCH partial updates, unified error JSON envelope.

## Tasks

### T01 — Todo model + repository

- **Inputs:** Assumed fields — UUID `id`, `title`, `completed`, `created_at`, `updated_at` (RFC 3339 UTC strings in JSON)
- **Outputs:** `Todo` serde struct; `TodoRepo` with `create`, `get`, `list(filter)`, `update`, `delete` using sqlx pool
- **Validation gate:** Repository tests with temp SQLite file
- **DoD:** Create assigns server UUID and timestamps; update refreshes `updated_at`

### T02 — POST /todos (create, 201)

- **Inputs:** JSON `{ "title": string, "completed"?: boolean }`
- **Outputs:** Handler returning `201` + Todo body
- **Validation gate:** Tests — happy path, trimmed title, `completed` default false, empty title 400, title > 200 chars 400
- **DoD:** Response uses `validation_error` code for bad input

### T03 — GET /todos (list + completed filter)

- **Inputs:** Optional query `completed=true` or `completed=false`
- **Outputs:** `200` JSON array (may be empty)
- **Validation gate:** Tests — no filter, `completed=true`, `completed=false`, invalid param → 400 `validation_error`
- **DoD:** Filter semantics match assumed answer Q5 (no pagination)

### T04 — GET /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `200` Todo or `404` with `not_found`
- **Validation gate:** Existing id + unknown id tests

### T05 — PATCH /todos/:id

- **Inputs:** `{ "title"?: string, "completed"?: boolean }` — at least one field required
- **Outputs:** `200` updated Todo; `400` empty body or title validation failure; `404` missing id
- **Validation gate:** Patch title only, completed only, both, empty body 400, 404

### T06 — DELETE /todos/:id (204)

- **Inputs:** Path UUID
- **Outputs:** `204` empty body on success; `404` `not_found`
- **Validation gate:** Delete then GET returns 404

### T07 — Error envelope helpers

- **Inputs:** Shape `{ "error": { "code", "message" } }`
- **Outputs:** Central error type mapping to Axum responses; codes `validation_error`, `not_found`, `internal_error`
- **Validation gate:** Assert error codes in handler tests
- **DoD:** Unexpected DB errors map to `internal_error` without leaking stack traces
