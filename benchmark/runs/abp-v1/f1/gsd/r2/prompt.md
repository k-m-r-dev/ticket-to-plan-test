# Benchmark prompt — protocol `abp-v1` arm `gsd` fixture `f1` r2

## Instructions

Follow skills/ticket-to-plan-gsd/SKILL.md with GSD MCP. Stop at plan-ready; do not implement.

## Skill

skills/ticket-to-plan-gsd/SKILL.md

## Fixture (Locked SPEC)

# Todo HTTP API — Locked Spec (Benchmark Fixture)

**Status:** LOCKED — do not re-open product decisions during planning.  
**Stack (fixed):** Rust, Axum, Tokio, SQLite via sqlx, JSON over HTTP.  
**Surface:** HTTP API only — no UI, no CLI client beyond optional curl examples in docs.

## Goal

Implement a local Todo HTTP API that persists todos in SQLite and exposes CRUD plus a completion filter.

## Data model

`Todo`:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | UUID string | Server-generated |
| `title` | string | Required; trimmed; length 1..=200 |
| `completed` | boolean | Default `false` on create |
| `created_at` | RFC 3339 UTC timestamp | Server-set |
| `updated_at` | RFC 3339 UTC timestamp | Server-set; updated on every successful PATCH |

## Endpoints

### `POST /todos`

- Body: `{ "title": string, "completed"?: boolean }`
- Success: `201` with full Todo JSON
- Validation failure: `400` with error shape below
- Empty/whitespace-only title or title longer than 200 → `400`

### `GET /todos`

- Query: optional `completed=true` or `completed=false`
- Success: `200` with JSON array of Todos (empty array allowed)
- Invalid `completed` value → `400`

### `GET /todos/:id`

- Success: `200` with Todo
- Missing id → `404`

### `PATCH /todos/:id`

- Body: any subset of `{ "title"?: string, "completed"?: boolean }`
- At least one field required; empty body → `400`
- Title rules same as create when `title` present
- Success: `200` with updated Todo
- Missing id → `404`

### `DELETE /todos/:id`

- Success: `204` empty body
- Missing id → `404`

## Error shape

All 4xx/5xx JSON responses:

```json
{ "error": { "code": "string_snake_case", "message": "human readable" } }
```

Required codes at minimum: `validation_error`, `not_found`, `internal_error`.

## Persistence

- SQLite file path configurable via `DATABASE_URL` (default `sqlite:todos.db`)
- Schema applied via sqlx migrations on startup
- Concurrent-safe enough for local single-process use (no multi-instance requirement)

## Server

- Bind `HOST` (default `127.0.0.1`) and `PORT` (default `8080`)
- `GET /health` → `200` `{ "status": "ok" }`

## Tests (required in any complete plan)

- Integration tests for: create, list, list filter, get, patch, delete
- Validation: empty title, overlong title, empty PATCH body, bad `completed` query
- 404 paths for get/patch/delete
- Prefer `axum` test / `tower` service tests or similar in-process HTTP tests

## Validation commands (for plans that include delivery)

- `cargo test`
- `cargo clippy -- -D warnings` (or project-equivalent once scaffolded)

## Out of scope (do not plan)

- Authentication / authorization
- Multi-user / tenancy
- Pagination, sorting beyond natural DB order
- Soft deletes
- Web UI / mobile client
- OpenAPI generation (optional mention is over-planning if tasked as required work)
- Docker / Kubernetes deployment
- Rate limiting, CORS policy beyond whatever Axum defaults need for local curl
- GraphQL / gRPC

## Planning instruction (all benchmark arms)

Produce a complete implementation plan from this document only. Do not ask clarifying product questions. Do not implement code in the planning run.


## Output

Write plan artifacts into `benchmark/runs/abp-v1/f1/gsd/r2/artifacts/`.
Fill meta.json started_at/ended_at, tool_calls, tokens when done.
