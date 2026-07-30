# M004: Todo HTTP API

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

**Out of scope:** Auth, multi-user, pagination/sorting, soft deletes, UI/CLI client, OpenAPI, Docker/K8s, rate limiting/CORS policy, GraphQL/gRPC.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | M004 |
| Scope slug | todo-http-api |
| Workstream | (single milestone; benchmark replicate r3) |
| External ticket | (none) |
| Integration strategy | feature-branch (from `.gsd/DELIVERY-PROFILE.md`) |
| Integration branch | main |
| Commit cadence | milestone — single commit after M004 verified; skill overrides profile `slice` cadence |
| Review unit | pr-per-milestone (from profile) |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` (in `apps/todo-api`) |
| Completion condition | SPEC met; S01–S03 verified; validation green; human approval before execution |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md`) — pause after each task, structured task report (task id/title, files changed, verification commands + outcomes, deviations/blockers), wait for explicit `do next`
- **Commit Gate** (`.gsd/workflow/milestone-workflow.md`) — commit only after the relevant scope (task/slice/unit per `commit_cadence`) is verified
- **Remote Mutation Rule** (`.gsd/workflow/milestone-workflow.md`) — no push, PR, or remote mutation without explicit user approval, gated further by the active Git/PR checkpoint mode
- **Validation Rule** (`.gsd/workflow/milestone-workflow.md`) — run the validation commands recorded in the Required Milestone Map before each commit and before each push
- **Commit Message Format** (`.gsd/workflow/milestone-workflow.md`) — `feat(todo-http-api): summary`; never use local planning IDs (`M004`, `S0x`) in commit messages or PR titles
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-gsd/SKILL.md`) — run every step of this skill in order; no partial runs
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-gsd/SKILL.md`) — `/grilling` and `/brainstorming` must be invocable; grilling skipped here because scope is fully specified
- **GSD Workflow MCP Planning Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — create milestone/slice/task plan artifacts only via GSD workflow MCP (`gsd_*`)
- **GSD Workflow MCP Execution Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — during execution, always use GSD workflow MCP for progress and state mutations (`gsd_progress`, `gsd_task_complete`, `gsd_slice_complete`, etc.)
- **GSD Artifact Completeness Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — create all files/artifacts GSD normally creates for milestone/slice/task; no partial trees
- **Full Plan Depth Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — plan must exist from workstream → milestone → slice → task before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-gsd/SKILL.md`) — do not commit at each slice complete; single commit per milestone after milestone verification; state this in each slice plan
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — embed these execution guardrails into the top-level unit's `## Delivery & Guardrails` and into each slice plan so later agents cannot miss them
