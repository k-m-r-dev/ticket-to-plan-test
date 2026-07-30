# M001 ROADMAP — Todo HTTP API (ABP f1, no-tools arm, replicate 2)

**Vision:** Deliver a local Todo HTTP API in Rust (Axum + Tokio + sqlx/SQLite) that satisfies the locked benchmark fixture with CRUD, completion filtering, validation, structured errors, and integration tests.

## Ambiguity & design approval

**Ambiguity gate:** Fixture f1 is fully specified — **grilling skipped**; no product decisions to reopen.

**Clarifying questions (would-have-asked):** None. Stack, endpoints, data model, error contract, persistence, configuration, and test expectations are locked in the fixture.

**Design approval:** Non-interactive benchmark run — planning artifacts pre-approved for scoring; **no implementation** in this session.

## Architecture overview

```text
┌─────────────┐     HTTP      ┌──────────────────┐
│   Client    │ ────────────► │  Axum Router     │
│  (curl)     │               │  /health         │
└─────────────┘               │  /todos CRUD     │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  Handlers        │
                              │  (validation)    │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  TodoRepository  │
                              │  (sqlx pool)     │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  SQLite          │
                              │  (migrations)    │
                              └──────────────────┘
```

## Success criteria

- `POST /todos` → `201` with full Todo JSON; title trimmed; length 1..=200; `completed` defaults `false`
- `GET /todos` → `200` array; optional `completed=true|false` filter; invalid query → `400`
- `GET /todos/:id` → `200` or `404`
- `PATCH /todos/:id` → `200` or `400`/`404`; at least one field required; `updated_at` refreshed on success
- `DELETE /todos/:id` → `204` or `404`
- `GET /health` → `200` `{ "status": "ok" }`
- Error JSON: `{ "error": { "code": "string_snake_case", "message": "human readable" } }` with `validation_error`, `not_found`, `internal_error`
- sqlx migrations on startup; `DATABASE_URL` (default `sqlite:todos.db`), `HOST` (default `127.0.0.1`), `PORT` (default `8080`)
- Integration tests: CRUD, filter, validation failures, 404 paths; `cargo test` + `cargo clippy -- -D warnings`

## Phases / slices

| Phase | Slice | Focus |
| --- | --- | --- |
| 1 | S01 | Project foundation: Cargo, sqlx SQLite, migrations, config, health |
| 2 | S02 | API handlers: Todo CRUD, filter, validation, error envelope |
| 3 | S03 | Integration test suite, clippy gate, milestone completion |

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
