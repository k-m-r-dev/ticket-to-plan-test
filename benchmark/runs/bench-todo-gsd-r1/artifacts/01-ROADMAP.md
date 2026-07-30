# M001: Todo HTTP API

**Vision:** Ship a locked Rust Axum+SQLite Todo HTTP API with CRUD, filter, validation, health, migrations, and integration tests — plan only, no UI/auth.

## Success Criteria

- POST/GET/PATCH/DELETE /todos and GET /health behave per fixtures/todo-api/SPEC.md
- sqlx migrations apply on startup
- cargo test covers CRUD, validation, and 404 paths
- cargo clippy -D warnings passes

## Slices

- [ ] **S01: Scaffold + persistence** `risk:medium` `depends:[]`
  > After this: Migrations create todos table; health responds

- [ ] **S02: Todo CRUD + filter + validation** `risk:medium` `depends:[S01]`
  > After this: curl CRUD and filtered list

- [ ] **S03: Integration tests + polish** `risk:low` `depends:[S02]`
  > After this: cargo test && cargo clippy -- -D warnings

## Boundary Map

In: Axum API + SQLite. Out: UI, auth, deploy.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | M001 |
| Scope slug | todo-http-api |
| Workstream | (single) |
| External ticket | (none) |
| Integration strategy | feature-branch |
| Integration branch | main |
| Commit cadence | milestone (single commit after milestone verified; skill overrides profile slice cadence) |
| Review unit | pr-per-milestone |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 → S02 → S03 |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | SPEC met + tests green; human approval before execution |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md`) — pause after each task; wait for `do next`
- **Commit Gate** (`.gsd/workflow/milestone-workflow.md`) — commit only after verified scope per cadence
- **Remote Mutation Rule** (`.gsd/workflow/milestone-workflow.md`) — no push/PR without approval
- **Validation Rule** (`.gsd/workflow/milestone-workflow.md`) — run validation commands before commit/push
- **Commit Message Format** (`.gsd/workflow/milestone-workflow.md`) — `feat(todo-http-api): summary`
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-gsd/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-gsd/SKILL.md`) — grilling + brainstorming (skipped grilling: scope fully specified)
- **GSD Workflow MCP Planning Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — plan via `gsd_*` only
- **GSD Workflow MCP Execution Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — progress via GSD MCP
- **GSD Artifact Completeness Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — full artifact tree
- **Full Plan Depth Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — milestone → slice → task
- **Milestone Commit Cadence** (`skills/ticket-to-plan-gsd/SKILL.md`) — single commit per milestone
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-gsd/SKILL.md`) — embed into ROADMAP and each slice plan

Scope is fully specified — no ambiguity to interrogate.
