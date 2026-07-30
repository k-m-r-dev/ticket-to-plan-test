## Why

The benchmark fixture requires a locked greenfield Todo HTTP API (Rust/Axum/SQLite) so ticket-to-plan arms can be compared on the same fully specified scope. Planning must capture a complete, apply-ready change before any implementation.

## What Changes

- Greenfield Axum + Tokio HTTP service with SQLite persistence via sqlx migrations
- Todo data model (UUID id, title, completed, created_at, updated_at) and CRUD endpoints
- Optional `completed` query filter on list; shared JSON error envelope
- `GET /health` and env-configurable `DATABASE_URL` / `HOST` / `PORT`
- In-process integration tests covering CRUD, validation, filters, and 404s

## Capabilities

### New Capabilities

- `todo-api`: HTTP Todo CRUD + list filter, health check, persistence, and error shape per locked SPEC

### Modified Capabilities

- (none — greenfield; no existing `openspec/specs/` requirements)

## Impact

- New crate at `apps/todo-api` (or equivalent greenfield path)
- Dependencies: axum, tokio, sqlx (sqlite), serde, uuid, chrono (or equivalent time crate)
- No auth, UI, pagination, soft deletes, or deployment packaging beyond a local binary

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID | `todo-http-api-abp-f1-r1` |
| Scope slug | `todo-http-api` |
| Workstream | (single change) |
| External ticket | (none) |
| Integration strategy | `feature-branch` (from `.gsd/DELIVERY-PROFILE.md`) |
| Integration branch | `main` |
| Commit cadence | `milestone` (skill override of profile `slice`) — single commit after whole change verified |
| Review unit | `pr-per-milestone` |
| Git/PR checkpoint mode | `milestone` |
| Branch name | `feature/todo-http-api` |
| Execution sequence | S01 scaffold+persistence → S02 CRUD+filter+errors → S03 tests+clippy |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | All SPEC endpoints + required tests green; plan approved; no code until apply |
| Size budget | ~800–1200 LOC application + tests |

### Guardrails

- **Task Handoff Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — pause after each task; wait for explicit `do next`
- **Commit Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — no push/PR without explicit user approval
- **Validation Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — run recorded validation commands before commit/push
- **Commit Message Format** (`skills/ticket-to-plan-openspec/SKILL.md`) — `feat(todo-http-api): summary`; never use internal change folder names alone as the only message
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — grilling + brainstorming required (available; grilling skipped — scope fully specified)
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — create artifacts only via OpenSpec CLI/`/opsx-*`
- **OpenSpec Artifact Completeness Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — all required change artifacts present
- **Full Plan Depth Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — proposal → specs → design → tasks before execution
- **Milestone Commit Cadence** (`skills/ticket-to-plan-openspec/SKILL.md`) — single commit per change after verification
- **Plan-Doc Embed Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — embed guardrails in proposal/design and summarize at top of `tasks.md`

## Scope note

Scope is fully specified — no ambiguity to interrogate (locked SPEC in fixture / prompt).
