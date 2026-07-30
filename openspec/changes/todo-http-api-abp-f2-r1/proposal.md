## Why

The ambiguous ticket requests a small local Todo HTTP API with persistence and validation, but leaves stack, routes, error shape, filtering, and auth unresolved. This change resolves those decisions and produces an apply-ready plan for a greenfield implementation without building code in the planning run.

## What Changes

- Greenfield **Rust / Axum / Tokio** HTTP service with **SQLite** persistence via **sqlx** migrations
- Todo CRUD at `/todos` plus `GET /health`; optional `completed` filter on list (no pagination)
- Shared JSON error envelope with `validation_error`, `not_found`, `internal_error`
- Title trim + length validation (1..=200); server-generated UUID and timestamps
- Env config: `DATABASE_URL`, `HOST`, `PORT`; one-command local run via `cargo run`
- In-process integration tests covering CRUD, validation, filter, and 404 paths
- **No auth**, UI, multi-tenant, or pagination in v1

## Capabilities

### New Capabilities

- `todo-api`: HTTP Todo CRUD, completion filter, health check, SQLite persistence, and error shape per resolved ticket decisions (see `CLARIFICATIONS.md` in run artifacts)

### Modified Capabilities

- (none — greenfield; no existing `openspec/specs/` requirements)

## Impact

- New crate at `apps/todo-api`
- Dependencies: axum, tokio, sqlx (sqlite + migrate), serde, uuid, chrono (or time)
- Local sqlite file survives restart; single-process concurrency acceptable for v1

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | `todo-http-api-abp-f2-r1` |
| Scope slug | `todo-http-api` |
| Workstream | (single change) |
| External ticket | ambiguous fixture `todo-api-ambiguous` |
| Integration strategy | `feature-branch` (from `.gsd/DELIVERY-PROFILE.md`) |
| Integration branch | `main` |
| Commit cadence | `milestone` (skill override of profile `slice`) — single commit after whole change verified |
| Review unit | `pr-per-milestone` |
| Git/PR checkpoint mode | `milestone` |
| Branch name | `feature/todo-http-api` |
| Execution sequence | S01 scaffold+persistence → S02 CRUD+filter+errors → S03 tests+clippy |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | All resolved endpoints + required tests green; plan approved; no code until apply |
| Size budget | ~800–1200 LOC application + tests |

### Guardrails

- **Task Handoff Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — pause after each task; wait for explicit `do next`
- **Commit Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — no push/PR without explicit user approval
- **Validation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — run recorded validation commands before commit/push
- **Commit Message Format** (`skills/ticket-to-plan-openspec/SKILL.md`) — `feat(todo-http-api): summary`; never use internal change folder names alone as the only message
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — grilling + brainstorming required (available; grilling documented as assumed answers — ticket ambiguous)
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — create artifacts only via OpenSpec CLI/`/opsx-*`
- **OpenSpec Artifact Completeness Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — all required change artifacts present
- **Full Plan Depth Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — proposal → specs → design → tasks before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-openspec/SKILL.md`) — single commit per change after verification
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — embed guardrails in `proposal.md`/`design.md` and summarize at top of `tasks.md`

## Scope note

Ticket is ambiguous — clarifying questions and assumed answers are recorded in run `artifacts/CLARIFICATIONS.md` and summarized in `design.md` Open Questions section. Matrix automation treats design approval as given for planning artifacts only.
