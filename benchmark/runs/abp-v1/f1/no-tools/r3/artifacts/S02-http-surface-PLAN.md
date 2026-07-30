# S02 — HTTP surface & business rules

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone**
- **Task Handoff Gate** — wait for `do next`
- **Validation Rule** — handler tests per endpoint where practical

## Goal

Expose all `/todos` endpoints with title validation, `completed` query filter, PATCH body rules, and a uniform JSON error envelope.

## Tasks

### T01 — Todo model and persistence layer

- **Inputs:** SPEC — UUID `id` (server-generated), `title`, `completed`, `created_at`, `updated_at` (RFC 3339 UTC)
- **Outputs:** `Todo` serde struct; repository with `insert`, `list`, `find`, `update_partial`, `delete` via sqlx
- **Validation gate:** Repository integration smoke against temp SQLite
- **DoD:** Create stamps both timestamps; successful PATCH refreshes `updated_at`

### T02 — POST /todos

- **Inputs:** Body `{ "title": string, "completed"?: boolean }`
- **Outputs:** `201` + full Todo; `400` + `validation_error` for empty/whitespace-only title or length > 200
- **Validation gate:** Tests — happy path, trim, empty title, overlong title, omitted `completed` defaults `false`
- **DoD:** Title trimmed before persist

### T03 — GET /todos with completed filter

- **Inputs:** Optional query `completed=true` or `completed=false`
- **Outputs:** `200` JSON array (empty allowed); `400` `validation_error` for invalid `completed` value
- **Validation gate:** Tests — unfiltered list, `completed=true`, `completed=false`, bad query param

### T04 — GET /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `200` Todo; `404` `not_found` when missing
- **Validation gate:** Existing resource + unknown UUID 404

### T05 — PATCH /todos/:id

- **Inputs:** Subset of `{ "title"?: string, "completed"?: boolean }`; at least one field required
- **Outputs:** `200` updated Todo; `400` for empty body or title validation failure; `404` missing id
- **Validation gate:** Patch title only, completed only, both, empty body 400, 404

### T06 — DELETE /todos/:id

- **Inputs:** Path UUID
- **Outputs:** `204` empty body; `404` `not_found`
- **Validation gate:** Delete then 404 on repeat GET

### T07 — Error envelope and status mapping

- **Inputs:** SPEC — all 4xx/5xx JSON: `{ "error": { "code", "message" } }`
- **Outputs:** `AppError` + `IntoResponse`; minimum codes: `validation_error`, `not_found`, `internal_error`
- **Validation gate:** Handler tests assert codes; unexpected DB errors map to `internal_error` without stack traces in body
- **DoD:** All handlers use shared error helper
