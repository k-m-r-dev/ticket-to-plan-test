# S02 — Todo CRUD + filter + validation

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone**
- **Task Handoff Gate** — wait for `do next`
- **Validation Rule** — unit/integration tests per handler where practical

## Goal

Implement all `/todos` endpoints, `completed` query filter, title validation, PATCH body rules, and consistent error JSON envelope.

## Tasks

### T01 — Domain model + repository layer

- **Inputs:** Assumed `Todo` fields and timestamps (UUID `id`, `title`, `completed`, `created_at`, `updated_at`)
- **Outputs:** `Todo` struct (serde), `TodoRepo` with create/read/list/update/delete against sqlx pool
- **Validation gate:** Repository unit tests or thin integration smoke test
- **DoD:** Server sets `id` (UUID), `created_at`, `updated_at` on create; `updated_at` refreshed on successful PATCH

### T02 — POST /todos

- **Inputs:** Body `{ "title": string, "completed"?: boolean }`
- **Outputs:** Handler returning `201` + full Todo JSON; `400` + `validation_error` for empty/whitespace-only or title > 200 chars
- **Validation gate:** Tests for happy path, trimmed title, empty title, overlong title
- **DoD:** `completed` defaults to `false` when omitted

### T03 — GET /todos (list + filter)

- **Inputs:** Optional query `completed=true` or `completed=false`
- **Outputs:** `200` JSON array (empty allowed); `400` `validation_error` for invalid `completed` value
- **Validation gate:** Tests for unfiltered list, `completed=true`, `completed=false`, bad query param

### T04 — GET /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `200` Todo; `404` `not_found` for missing id
- **Validation gate:** Get existing + 404 test

### T05 — PATCH /todos/:id

- **Inputs:** Body subset of `{ "title"?: string, "completed"?: boolean }`; at least one field required
- **Outputs:** `200` updated Todo; `400` for empty body or title validation failure; `404` missing id
- **Validation gate:** Patch title, patch completed, empty body 400, 404

### T06 — DELETE /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `204` empty body; `404` `not_found`
- **Validation gate:** Delete success + 404

### T07 — Error envelope middleware/helpers

- **Inputs:** Assumed error shape `{ "error": { "code", "message" } }`
- **Outputs:** Central mapping to JSON responses for 4xx/5xx
- **Validation gate:** Assert codes `validation_error`, `not_found`, `internal_error` appear in tests
- **DoD:** Unexpected DB/panic paths map to `internal_error` (no stack traces in response)
