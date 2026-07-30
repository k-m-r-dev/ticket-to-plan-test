# M001: Todo HTTP API

**Vision:** Ship a locked Rust Axum+SQLite Todo HTTP API with CRUD, completion filter, validation, health, sqlx migrations, and in-process integration tests. Plan only — no UI, auth, or deploy.

## Success Criteria

- POST/GET/PATCH/DELETE /todos and GET /health match the locked SPEC
- SQLite schema applied via sqlx migrations on startup; DATABASE_URL/HOST/PORT configurable
- Integration tests cover create, list, filter, get, patch, delete, validation, and 404 paths
- cargo test and cargo clippy -- -D warnings pass

## Slices

- [ ] **S01: Scaffold + persistence** `risk:medium` `depends:[]`
  > After this: Migrations create todos table; GET /health returns 200

- [ ] **S02: Todo CRUD + filter + validation** `risk:medium` `depends:[S01]`
  > After this: curl CRUD and filtered list with correct status codes

- [ ] **S03: Integration tests + polish** `risk:low` `depends:[S02]`
  > After this: cargo test && cargo clippy -- -D warnings

## Boundary Map

**In:** Rust Axum HTTP API, SQLite via sqlx, migrations, JSON CRUD + completed filter, health, integration tests.

## Out of scope

Auth, multi-user, pagination/sorting, soft deletes, UI/CLI client, OpenAPI, Docker/K8s, rate limiting/CORS policy, GraphQL/gRPC.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | M001 |
| Scope slug | todo-http-api |
| Workstream | (single milestone) |
| External ticket | (none) |
| Integration strategy | branch-per-milestone (profile `feature-branch` mapped) |
| Integration branch | main |
| Commit cadence | milestone — single commit after M001 verified; skill overrides profile `slice` cadence |
| Review unit | milestone (profile `pr-per-milestone`) |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` (in `apps/todo-api`) |
| Completion condition | SPEC met; S01–S03 verified; validation green; human approval before execution |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md`) — pause after each task, structured task report, wait for explicit `do next`
- **Commit Gate** (`.gsd/workflow/milestone-workflow.md`) — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** (`.gsd/workflow/milestone-workflow.md`) — no push/PR/remote mutation without explicit user approval
- **Validation Rule** (`.gsd/workflow/milestone-workflow.md`) — run Required Milestone Map validation commands before each commit and push
- **Commit Message Format** (`.gsd/workflow/milestone-workflow.md`) — `feat(todo-http-api): summary`; never use local IDs `M001`/`S0x` in commits or PR titles
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-gsd/SKILL.md`) — run every step in order; no partial runs
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-gsd/SKILL.md`) — `/grilling` and `/brainstorming` invocable; grilling skipped here because scope is fully specified
- **GSD Workflow MCP Planning Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — create milestone/slice/task artifacts only via `gsd_*`
- **GSD Workflow MCP Execution Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — progress/state mutations via GSD MCP (`gsd_progress`, `gsd_task_complete`, etc.)
- **GSD Artifact Completeness Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — full milestone/slice/task artifact tree
- **Full Plan Depth Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — workstream → milestone → slice → task before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-gsd/SKILL.md`) — do not commit at each slice complete; single commit per milestone after verification
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — embed these guardrails into ROADMAP and each slice plan
