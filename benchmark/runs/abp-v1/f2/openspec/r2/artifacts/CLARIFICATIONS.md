# Clarifying questions (grilling) — assumed answers

Non-interactive run: questions below would have been asked one at a time via `/grilling`. Assumed answers recorded before planning.

## Stack and runtime

| Question | Assumed answer |
| --- | --- |
| Language / framework? | **Rust** with **Axum** on **Tokio** — small binary, team can `cargo run`, strong typing for validation. |
| Database product? | **SQLite** via **sqlx** with migrations — local file persistence, no separate DB server. |
| How to run with one command? | `cd apps/todo-api && cargo run` (env overrides for `DATABASE_URL`, `HOST`, `PORT`). |

## API surface

| Question | Assumed answer |
| --- | --- |
| Exact URL paths? | `POST /todos`, `GET /todos`, `GET /todos/:id`, `PATCH /todos/:id`, `DELETE /todos/:id`, `GET /health`. |
| Status codes? | Create **201**; read/list/patch **200**; delete success **204**; validation **400**; missing todo **404**; unexpected server fault **500**. |
| Error JSON shape? | `{"error":{"code":"<string>","message":"<string>"}}` with codes `validation_error`, `not_found`, `internal_error`. |
| Filtering / pagination? | Optional `completed=true\|false` on `GET /todos`; **no pagination** or sorting in v1. |
| Auth? | **No auth** — local single-user; document as non-goal. |

## Data model and validation

| Question | Assumed answer |
| --- | --- |
| Todo fields? | `id` (UUID string), `title` (string), `completed` (bool), `created_at` / `updated_at` (RFC3339 strings). |
| Title validation? | Trim whitespace; reject empty/whitespace-only or length **> 200** with `validation_error`. |
| PATCH rules? | Body subset of `title` / `completed`; require **≥1** field; apply title rules when `title` present; bump `updated_at`. |
| Invalid `completed` query? | `400 validation_error` when `completed` query param is not `true` or `false`. |

## Config

| Question | Assumed answer |
| --- | --- |
| Configuration? | `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`). |

## Brainstorming — structural gaps addressed in plan

- **Empty list:** `GET /todos` returns `[]` when no rows — not an error.
- **Restart persistence:** sqlx migrations on startup; data in sqlite file survives process restart.
- **Concurrency:** last-write-wins on PATCH; acceptable for local single-user v1.
- **Tests:** in-process axum/tower tests with temp sqlite + migrations (not separate test DB server).
- **Idempotency:** DELETE missing id → 404; repeated DELETE not required to be idempotent beyond 404.
- **Observability:** `/health` for liveness only; no metrics stack in v1.

## Out of scope (non-goals)

No auth, multi-tenant tenancy, mobile client, UI, OpenAPI artifact, Docker/K8s deploy, GraphQL/gRPC, rate limiting/CORS policy, pagination beyond completed filter, soft deletes.

## Design approval

Matrix automation treats human approval as given for **planning artifacts only**. Execution still requires explicit `do next` per Task Handoff Gate.
