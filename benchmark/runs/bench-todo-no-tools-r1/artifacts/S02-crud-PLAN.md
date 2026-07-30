# S02 — Todo CRUD + filter + validation

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone**
- **Task Handoff Gate** — wait for `do next`
- **Validation Rule** — `cargo test`

## Goal

POST/GET/PATCH/DELETE `/todos`, `completed` filter, error JSON shape.

## Tasks

### T01 POST /todos
- Validation title 1..=200; 201 Todo; 400 `validation_error`
- Validation gate: create + empty title tests

### T02 GET /todos + filter
- `?completed=true|false`; invalid → 400
- Validation: list + filter tests

### T03 GET/PATCH/DELETE by id
- 404 `not_found`; PATCH needs ≥1 field; DELETE 204
- Validation: get/patch/delete + 404 tests

### T04 Error envelope
- `{ "error": { "code", "message" } }` with `validation_error`, `not_found`, `internal_error`
- Validation: assert envelope
