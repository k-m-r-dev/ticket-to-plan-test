# Proposal: todo-http-api

## Why

Benchmark fixture requires a locked Rust HTTP Todo API (Axum + SQLite/sqlx) so planning arms can be compared. This change captures the full plan before any implementation.

## What changes

- Greenfield Axum service with SQLite persistence via sqlx migrations
- Todo CRUD endpoints + `completed` list filter + `/health`
- Shared JSON error shape (`validation_error`, `not_found`, `internal_error`)
- Integration tests for CRUD, validation, and 404s

## Non-goals

- Authentication, UI, pagination, Docker/K8s, GraphQL/gRPC, OpenAPI as required work

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | todo-http-api |
| Scope slug | todo-http-api |
| Workstream | (single change) |
| External ticket | (none) |
| Integration strategy | feature-branch |
| Integration branch | main |
| Commit cadence | milestone (single commit after change verified) |
| Review unit | pr-per-milestone |
| Git/PR checkpoint mode | milestone |
| Branch name | feature/todo-http-api |
| Execution sequence | S01 scaffold → S02 CRUD → S03 tests |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | SPEC endpoints + tests green; human approval before apply |
| Size budget | ~800–1200 LOC |

### Guardrails

- **Task Handoff Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — pause after each task; wait for `do next`
- **Commit Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — commit only after verified change scope
- **Remote Mutation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — no push/PR without explicit approval
- **Validation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — run validation commands before commit/push
- **Commit Message Format** (`skills/ticket-to-plan-openspec/SKILL.md`) — `feat(todo-http-api): summary`
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — grilling + brainstorming available (skipped: scope fully specified)
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — artifacts via OpenSpec only
- **OpenSpec Artifact Completeness Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — proposal/specs/design/tasks present
- **Full Plan Depth Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — proposal → specs → design → tasks before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-openspec/SKILL.md`) — single commit per change after verification
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — guardrails embedded here and in tasks.md

## Scope note

Scope is fully specified — no ambiguity to interrogate (`fixtures/todo-api/SPEC.md`).
