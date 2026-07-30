# Design summary — Todo HTTP API (native arm, f2)

**Ambiguity:** Fixture f2 is intentionally incomplete. This session is **non-interactive** — each open question from the ticket is recorded below with the answer assumed to proceed.

## Clarifying questions (would-have-asked) and assumed answers

| # | Question | Assumed answer | Rationale |
| --- | --- | --- | --- |
| Q1 | **Language / framework?** | **Rust + Axum + Tokio** | Single static binary, strong typing for validation, idiomatic small HTTP service; team can run with `cargo run`. |
| Q2 | **Database product?** | **SQLite via sqlx** | Local single-user use; file-backed persistence survives restart; no external services. |
| Q3 | **Exact URL paths and status codes?** | REST: `POST/GET/PATCH/DELETE /todos`, `GET /todos/:id`, `GET /health`; `201` create, `200` read/update, `204` delete, `400` validation, `404` not found | Conventional REST mapping keeps curl examples simple. |
| Q4 | **Error JSON shape?** | `{ "error": { "code": "string_snake_case", "message": "human readable" } }` with at least `validation_error`, `not_found`, `internal_error` | Consistent machine + human readable errors for local debugging. |
| Q5 | **Filtering / pagination?** | Optional `completed=true\|false` query on `GET /todos`; **no pagination** | Ticket asks for complete/incomplete marking; local list sizes don't need pages yet. |
| Q6 | **Auth?** | **None** — bind to localhost by default; single-user local API | Ticket allows single-user local use; auth deferred. |
| Q7 | **Todo data model?** | `id` (UUID, server-generated), `title` (trimmed, 1..=200 chars), `completed` (bool, default false), `created_at` / `updated_at` (RFC 3339 UTC) | Minimal fields covering CRUD + completion toggle with audit timestamps. |
| Q8 | **One-command run?** | `cargo run` after initial compile; env vars `DATABASE_URL`, `HOST`, `PORT` with sensible defaults | Satisfies “run with one command” constraint. |

**Approach:** Thin Axum service with sqlx-backed SQLite, env-driven config, and in-process integration tests (`axum::test` / tower `ServiceExt`). Project root `apps/todo-api/`. Layered modules: `config`, `db`, `models`, `error`, `routes`.

**Design approval:** Non-interactive benchmark run — planning artifacts pre-approved for scoring; **no implementation** in this session.

## Out of scope (non-goals)

Authentication / authorization, multi-user tenancy, pagination beyond natural DB order, sorting controls, soft deletes, web UI, mobile client, OpenAPI as required deliverable, Docker/Kubernetes, rate limiting, CORS policy beyond local curl, GraphQL/gRPC. **No auth** for v1.
