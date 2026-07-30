# M007: Local Todo HTTP API

**Vision:** Resolve ambiguous ticket via CLARIFICATIONS.md, then ship Rust Axum+SQLite local Todo HTTP API with CRUD, completed filter, validation, health, sqlx migrations, and integration tests. Single-user local use; no auth, UI, or deploy.

## Success Criteria

- POST/GET/PATCH/DELETE /todos and GET /health match assumed API contract in CLARIFICATIONS.md
- SQLite schema via sqlx migrations on startup; DATABASE_URL/HOST/PORT configurable
- Integration tests cover create, list, filter, get, patch, delete, validation, and 404 paths
- cargo test and cargo clippy -- -D warnings pass in apps/todo-api

## Slices

- [ ] **S01: Scaffold + persistence** `risk:medium` `depends:[]`
  > After this: Migrations create todos table; GET /health returns 200

- [ ] **S02: Todo CRUD + filter + validation** `risk:medium` `depends:[S01]`
  > After this: curl CRUD and filtered list with correct status codes

- [ ] **S03: Integration tests + polish** `risk:low` `depends:[S02]`
  > After this: cargo test && cargo clippy -- -D warnings

## Boundary Map

**In:** Rust Axum HTTP API, SQLite via sqlx, migrations, JSON CRUD + completed filter, health, integration tests.

**Out of scope:** Auth, multi-user tenancy, pagination/sorting, soft deletes, UI client, OpenAPI artifact, Docker/K8s, rate limiting/CORS, GraphQL/gRPC.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Milestone / planning ID | M007 |
| Human-readable scope slug | local-todo-http-api |
| Workstream name | (single milestone) |
| External ticket ID | (none) |
| Integration strategy | feature-branch (profile `feature-branch`) |
| Integration branch | main |
| Commit cadence | milestone — single commit after M007 verified; skill overrides profile `slice` cadence |
| Review unit | pr-per-milestone |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/local-todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cd apps/todo-api && cargo test`; `cd apps/todo-api && cargo clippy -- -D warnings` |
| Completion condition | CLARIFICATIONS contract met; S01–S03 verified; validation green; human approval before execution |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md`) — pause after each task, structured task report, wait for explicit `do next`
- **Commit Gate** (`.gsd/workflow/milestone-workflow.md`) — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** (`.gsd/workflow/milestone-workflow.md`) — no push, PR, or remote mutation without explicit user approval
- **Validation Rule** (`.gsd/workflow/milestone-workflow.md`) — run validation commands before each commit and push
- **Commit Message Format** (`.gsd/workflow/milestone-workflow.md`) — `feat(local-todo-http-api): summary`; never use local IDs `M007`/`S0x` in commits or PR titles
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-gsd/SKILL.md`) — run every step in order; no partial runs
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-gsd/SKILL.md`) — `/grilling` and `/brainstorming` invocable; grilling simulated via CLARIFICATIONS.md (non-interactive)
- **GSD Workflow MCP Planning Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — milestone/slice/task artifacts via `gsd_*` MCP
- **GSD Workflow MCP Execution Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — progress/state via GSD MCP (`gsd_progress`, `gsd_task_complete`, etc.)
- **GSD Artifact Completeness Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — full milestone/slice/task artifact tree
- **Full Plan Depth Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — workstream → milestone → slice → task before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-gsd/SKILL.md`) — do not commit at each slice complete; single commit per milestone after verification
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — embed guardrails in ROADMAP and each slice plan
