# M001 ROADMAP — Todo HTTP API (ABP f1, no-tools arm)

**Vision:** Greenfield Rust Axum + SQLite Todo HTTP API per locked benchmark fixture (`fixtures/todo-api`).

## Ambiguity & design approval

**Ambiguity gate:** Fixture f1 is fully specified — **grilling skipped**; no product decisions to reopen.

**Clarifying questions (would-have-asked):** None. All stack, endpoints, validation rules, error shape, persistence, config, and test expectations are locked in the fixture.

**Design approval:** Non-interactive benchmark run — planning artifacts pre-approved for scoring; **no implementation** in this session.

## Success criteria

- `POST` / `GET` / `PATCH` / `DELETE` `/todos` and `GET /health` match locked SPEC
- `Todo` model: UUID `id`, `title` (trimmed, 1..=200), `completed` (default false), RFC 3339 `created_at` / `updated_at`
- sqlx migrations applied on startup; `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`)
- Error JSON: `{ "error": { "code": "string_snake_case", "message": "human readable" } }` with at least `validation_error`, `not_found`, `internal_error`
- Integration tests: CRUD, `completed` filter, validation failures, 404 paths
- `cargo test` and `cargo clippy -- -D warnings` pass

## Slices

| Slice | Focus |
| --- | --- |
| S01 | Cargo scaffold, sqlx SQLite schema + migrations, config, health endpoint |
| S02 | Todo CRUD handlers, query filter, validation, error envelope |
| S03 | Integration test suite + clippy polish |

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | M001 |
| Scope slug | todo-http-api |
| Workstream | (single) |
| External ticket | (none — benchmark fixture) |
| Integration strategy | feature-branch |
| Integration branch | main |
| Commit cadence | milestone |
| Review unit | pr-per-milestone |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | All SPEC behaviors covered by tests; clippy clean; human approval before first commit |
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

## Out of scope (do not implement)

Authentication, multi-user tenancy, pagination/sorting beyond DB order, soft deletes, web UI, OpenAPI as required work, Docker/Kubernetes, rate limiting/CORS policy beyond local curl needs, GraphQL/gRPC.
