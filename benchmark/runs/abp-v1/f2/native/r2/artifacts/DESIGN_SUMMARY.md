# Design summary — Local Todo HTTP API (native arm, f2 r2)

**Fixture:** Ambiguous ticket (`fixtures/todo-api-ambiguous/TICKET.md`).  
**Session mode:** Non-interactive — clarifying questions and assumed answers are recorded below; no stakeholder input was available.

## Clarifying questions and assumed answers

| # | Open question (from ticket) | Assumed answer | Rationale |
| --- | --- | --- | --- |
| Q1 | Language / framework? | **Rust** with **Axum** on **Tokio** | Small, fast local binary; strong validation; `cargo run` satisfies one-command constraint. |
| Q2 | Database product? | **SQLite** via **sqlx** | File-backed persistence survives restart; no external DB process for single-user local use. |
| Q3 | Exact URL paths and status codes? | `GET /health`; `POST /todos` → `201`; `GET /todos` → `200`; `GET /todos/:id` → `200`; `PATCH /todos/:id` → `200`; `DELETE /todos/:id` → `204`; validation → `400`; missing resource → `404` | Conventional REST keeps curl smoke tests simple. |
| Q4 | Error JSON shape? | `{ "error": { "code": "snake_case", "message": "string" } }` with codes `validation_error`, `not_found`, `internal_error` | Machine-readable codes plus human messages for local debugging. |
| Q5 | Filtering / pagination? | Optional `completed=true` or `completed=false` on `GET /todos`; **no pagination** | Completion toggle is in scope; local lists do not need paging yet. |
| Q6 | Auth? | **None** — bind `127.0.0.1` by default; single-user local API | Ticket allows single-user local use; auth is deferred. |
| Q7 | Todo fields? | `id` (UUID, server-generated), `title` (trimmed, 1..=200 chars), `completed` (bool, default `false`), `created_at` / `updated_at` (RFC 3339 UTC) | Covers CRUD, completion toggle, and basic audit timestamps. |
| Q8 | One-command run? | `cargo run` from `apps/todo-api/` after initial build; env `DATABASE_URL`, `HOST`, `PORT` with defaults | Meets “run with one command” after compile. |

## Architecture overview

Thin Axum router over a sqlx SQLite repository. Layers: `config` (env), `db` (pool + migrations), `models` + repository, `error` (JSON envelope), `routes` (`health`, `todos`). Integration tests use in-process HTTP against isolated SQLite per test.

**Project root:** `apps/todo-api/`

**Design approval:** Non-interactive benchmark — planning artifacts only; **no implementation** in this session.

## Out of scope (non-goals)

Authentication / authorization, multi-user tenancy, pagination, custom sorting, soft deletes, web UI, mobile client, OpenAPI as required deliverable, Docker/Kubernetes, rate limiting, CORS beyond local curl, GraphQL/gRPC. **No auth** for v1.
