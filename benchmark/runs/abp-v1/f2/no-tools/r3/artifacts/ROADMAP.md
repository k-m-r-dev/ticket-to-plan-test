# M001 ROADMAP — Local Todo HTTP API (ABP f2, no-tools r3)

**Vision:** Greenfield single-user Todo HTTP API with durable SQLite storage. Ambiguous ticket resolved through documented grilling assumptions; brainstorming selects a minimal Axum + sqlx vertical slice. Planning-only benchmark run — no implementation.

## Ambiguity gate (grilling + brainstorming)

Fixture f2 is **ambiguous** — `/grilling` and `/brainstorming` are required per `skills/ticket-to-plan-no-tools/SKILL.md`. This session is **non-interactive**; each open ticket question is recorded with the answer assumed to proceed.

### Clarifying questions and assumed answers

| # | Open question (from ticket) | Assumed answer | Rationale |
| --- | --- | --- | --- |
| Q1 | Language / framework? | **Rust** + **Axum** on **Tokio** | Small static binary, strong validation, idiomatic HTTP; team runs with `cargo run`. |
| Q2 | Database product? | **SQLite** via **sqlx** | File-backed persistence survives restart; no external DB service for local use. |
| Q3 | Exact URL paths and status codes? | `POST /todos` → 201; `GET /todos` → 200; `GET /todos/:id` → 200/404; `PATCH /todos/:id` → 200/400/404; `DELETE /todos/:id` → 204/404; `GET /health` → 200 | REST resource layout; predictable curl examples. |
| Q4 | Error JSON shape? | `{ "error": { "code": "<snake_case>", "message": "<string>" } }` with codes `validation_error`, `not_found`, `internal_error` | Machine-readable codes plus human messages for local debugging. |
| Q5 | Filtering / pagination? | Optional `completed=true\|false` on `GET /todos`; **no pagination** in v1 | Completion toggle is a stated goal; local lists stay small. |
| Q6 | Auth? | **None** — default bind `127.0.0.1`; single-user local API | Ticket allows local single-user use; auth deferred. |
| Q7 | Todo fields? | `id` (UUID, server-generated), `title` (trimmed, 1..=200 chars), `completed` (bool, default false), `created_at` / `updated_at` (RFC 3339 UTC) | Covers CRUD, completion marking, and audit timestamps. |
| Q8 | One-command run? | `cargo run` after initial `cargo build`; env `DATABASE_URL`, `HOST`, `PORT` with defaults | Satisfies “run with one command” post-compile. |

**Brainstorming outcome:** Thin Axum service, sqlx migrations at startup, in-process integration tests via Axum test client — smallest path to persistence, validation, and restart safety without auth, UI, or deployment tooling.

**Design approval:** Non-interactive benchmark — planning artifacts approved for scoring; **no code** in this session.

## Success criteria

- Full CRUD on `/todos` plus `GET /health` per assumed contract
- `Todo` JSON: UUID `id`, `title` (trimmed, 1..=200), `completed` (default false), RFC 3339 `created_at` / `updated_at`
- sqlx migrations on startup; `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`)
- `GET /todos?completed=true|false` filter; invalid query → `validation_error`
- PATCH requires at least one of `title` or `completed`; empty body → 400
- Error envelope on all failure paths; no stack traces in responses
- Integration tests cover CRUD, filter, validation failures, and 404 paths
- `cargo test` and `cargo clippy -- -D warnings` pass before milestone commit

## API contract (assumed)

| Method | Path | Success | Body / notes |
| --- | --- | --- | --- |
| POST | `/todos` | 201 | `{ "title", "completed?" }` → full Todo |
| GET | `/todos` | 200 | Array; optional `?completed=true\|false` |
| GET | `/todos/:id` | 200 / 404 | Single Todo |
| PATCH | `/todos/:id` | 200 / 400 / 404 | Partial `{ "title?", "completed?" }` |
| DELETE | `/todos/:id` | 204 / 404 | Empty body on success |
| GET | `/health` | 200 | `{ "status": "ok" }` |

## Slices

| Slice | Focus |
| --- | --- |
| S01 | Project scaffold, sqlx SQLite + migrations, config, health |
| S02 | Todo repository, CRUD handlers, filter, validation, error mapping |
| S03 | Integration tests, clippy gate, milestone readiness |

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
| Completion condition | All success criteria met by tests; clippy clean; human approval before first commit |
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

Authentication / authorization, multi-user tenancy, pagination, sorting controls, soft deletes, web UI, mobile client, OpenAPI as required deliverable, Docker/Kubernetes, rate limiting, CORS policy beyond local curl, GraphQL/gRPC. **No auth** for v1.
