# M001 ROADMAP — Todo HTTP API (ABP f2, no-tools arm)

**Vision:** Greenfield local Todo HTTP API with SQLite persistence — stack and API contract resolved from ambiguous ticket via grilling + brainstorming (non-interactive assumed answers).

## Ambiguity & design approval

**Ambiguity gate:** Fixture f2 is intentionally incomplete — **grilling + brainstorming required**. This session is non-interactive; each open question is recorded below with the answer assumed to proceed.

### Clarifying questions (would-have-asked) and assumed answers

| # | Question | Assumed answer | Rationale |
| --- | --- | --- | --- |
| Q1 | **Language / framework?** | **Rust + Axum + Tokio** | Single static binary, strong typing for validation, team can run with `cargo run`; Axum is idiomatic for small HTTP services. |
| Q2 | **Database product?** | **SQLite via sqlx** | Local single-user use; zero external services; file-backed persistence survives restart; migrations on startup. |
| Q3 | **Exact URL paths and status codes?** | REST: `POST/GET/PATCH/DELETE /todos`, `GET /todos/:id`, `GET /health`; `201` create, `200` read/update, `204` delete, `400` validation, `404` not found | Conventional REST mapping keeps curl examples simple. |
| Q4 | **Error JSON shape?** | `{ "error": { "code": "string_snake_case", "message": "human readable" } }` with at least `validation_error`, `not_found`, `internal_error` | Consistent machine + human readable errors for local debugging. |
| Q5 | **Filtering / pagination?** | Optional `completed=true\|false` query on `GET /todos`; **no pagination** | Ticket asks for complete/incomplete marking; local list sizes don't need pages yet. |
| Q6 | **Auth?** | **None** — bind to localhost by default; single-user local API | Ticket allows single-user local use; auth deferred. |
| Q7 | **Todo data model?** | `id` (UUID, server-generated), `title` (trimmed, 1..=200 chars), `completed` (bool, default false), `created_at` / `updated_at` (RFC 3339 UTC) | Minimal fields covering CRUD + completion toggle with audit timestamps. |
| Q8 | **One-command run?** | `cargo run` after `cargo build`; env vars `DATABASE_URL`, `HOST`, `PORT` with sensible defaults | Satisfies “run with one command” after initial compile. |

**Brainstorming summary:** A thin Axum service with sqlx-backed SQLite, env-driven config, and in-process integration tests (`axum::test` / tower `ServiceExt`) gives the smallest vertical slice that meets persistence, validation, and restart safety without auth, UI, or deployment complexity.

**Design approval:** Non-interactive benchmark run — planning artifacts pre-approved for scoring; **no implementation** in this session.

## Success criteria

- `POST` / `GET` / `PATCH` / `DELETE` `/todos`, `GET /todos/:id`, `GET /health` per assumed contract above
- `Todo` model: UUID `id`, `title` (trimmed, 1..=200), `completed` (default false), RFC 3339 `created_at` / `updated_at`
- sqlx migrations applied on startup; `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`)
- Error JSON envelope with `validation_error`, `not_found`, `internal_error`
- Integration tests: CRUD, `completed` filter, validation failures, 404 paths
- `cargo test` and `cargo clippy -- -D warnings` pass

## Slices

| Slice | Focus |
| --- | --- |
| S01 | Cargo scaffold, sqlx SQLite schema + migrations, config, health endpoint |
| S02 | Todo CRUD handlers, `completed` query filter, validation, error envelope |
| S03 | Integration test suite + clippy polish |

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | M001 |
| Scope slug | todo-http-api |
| Workstream | (single) |
| External ticket | fixtures/todo-api-ambiguous/TICKET.md |
| Integration strategy | feature-branch |
| Integration branch | main |
| Commit cadence | milestone |
| Review unit | pr-per-milestone |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | All assumed behaviors covered by tests; clippy clean; human approval before first commit |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — pause after each task; wait for `do next`
- **Commit Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — commit only after verified milestone scope per cadence
- **Remote Mutation Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — no push/PR without explicit approval
- **Validation Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — run validation commands before commit/push
- **Commit Message Format** (`skills/ticket-to-plan-no-tools/SKILL.md`) — `feat(todo-http-api): summary`
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-no-tools/SKILL.md`)
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`)
- **No External Planning Tools Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — markdown artifacts only; no GSD MCP / OpenSpec CLI
- **Full Plan Depth Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — milestone → slice → task before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-no-tools/SKILL.md`) — single commit per milestone
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — copy guardrails into each slice plan

## Out of scope (non-goals)

Authentication / authorization, multi-user tenancy, pagination beyond natural DB order, sorting controls, soft deletes, web UI, mobile client, OpenAPI as required deliverable, Docker/Kubernetes, rate limiting, CORS policy beyond local curl, GraphQL/gRPC. **No auth** for v1.
