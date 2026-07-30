## Context

See `proposal.md` — Why/What Changes. The repo already contains an `apps/todo-api` skeleton crate (placeholder `main.rs`); this change replaces the stub with a full Axum + sqlx implementation. Constraints are fixed by the locked fixture: Rust + Axum + Tokio + SQLite via `sqlx`, JSON over HTTP, no UI/CLI beyond curl examples.

## Goals / Non-Goals

**Goals:**
- Deliver the full CRUD + filter surface from `specs/todo-api/spec.md` with correct validation, error shape, and persistence semantics.
- Keep the implementation simple enough for a single local process (no multi-instance coordination).

**Non-Goals:**
- Authentication/authorization, multi-tenancy, pagination/sorting, soft deletes, Web/mobile UI, OpenAPI generation, containerized deployment, rate limiting/CORS beyond Axum defaults — all excluded per the locked fixture's "Out of scope" list.

## Decisions

- **Crate location**: implement in existing `apps/todo-api/` rather than creating a new top-level crate. *Alternative considered*: fresh crate at repo root — rejected because the benchmark workspace already reserves `apps/todo-api` for this fixture and the oracle tests expect that layout.
- **Module layout**: `src/main.rs` (startup + bind), `src/app.rs` (router factory), `src/handlers/todos.rs`, `src/handlers/health.rs`, `src/models.rs`, `src/error.rs`, `src/db.rs`, `src/config.rs`. *Alternative considered*: flat `handlers.rs` — rejected to keep health and todo routes separated as the surface grows.
- **IDs**: `uuid::Uuid` generated server-side with `Uuid::new_v4()`, stored/returned as string per fixture.
- **Timestamps**: `chrono::DateTime<Utc>` serialized as RFC 3339 via `serde`; `updated_at` refreshed on every successful PATCH.
- **Validation**: inline helpers in `models.rs` — trim + length check for title (1..=200 after trim), strict `"true"`/`"false"` parsing for `completed` query, reject empty PATCH body when both fields absent.
- **Error handling**: `AppError` enum implementing `IntoResponse`, mapping to `{validation_error: 400, not_found: 404, internal_error: 500}` with `{ "error": { "code", "message" } }` body.
- **Persistence**: `sqlx::SqlitePool` with `sqlx::migrate!` at startup; `DATABASE_URL` from env defaulting to `sqlite:todos.db`.
- **Testing**: integration tests in `apps/todo-api/tests/` using `axum::Router` + `tower::ServiceExt::oneshot` against `sqlite::memory:` or per-test temp files for isolation.

## Risks / Trade-offs

- [Parallel test runs against shared SQLite file] → Mitigation: default tests to in-memory SQLite or unique temp paths via `tempfile` crate.
- [Strict boolean query parsing] → Mitigation: only accept exact `"true"`/`"false"`; all other values return `400 validation_error`.
- [Skeleton crate may lack Cargo.toml deps] → Mitigation: first task adds all required dependencies before handler work begins.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID / change name | `todo-http-api-abp-f1-r3` |
| Scope slug | `todo-http-api` |
| Workstream | n/a (single change) |
| External ticket ID | none (benchmark fixture, no tracker) |
| Integration strategy | `feature-branch` (per `.gsd/DELIVERY-PROFILE.md`) |
| Integration branch | `main` |
| Commit cadence | `milestone` — single commit after the whole change is verified (this skill's fixed cadence; overrides the repo default `slice` cadence) |
| Review unit | `pr-per-milestone` (per `.gsd/DELIVERY-PROFILE.md`) |
| Git/PR checkpoint mode | `milestone` |
| Branch name | `feat/todo-http-api-abp-f1-r3` |
| Execution sequence | Expand skeleton deps → migrations/db → models/error → handlers/router → integration tests → clippy/test pass → single commit |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` (run from `apps/todo-api/`) |
| Completion condition | All tasks in `tasks.md` checked, `cargo test` and `cargo clippy -- -D warnings` pass |
| Size budget | Single crate under `apps/todo-api`, ~8-10 source files, no more than ~700 LOC excluding tests |

### Guardrails (cited, not restated)

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md` if present, else this skill) — pause after each task; wait for explicit `do next`
- **Commit Gate** — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** — no push/PR without explicit user approval
- **Validation Rule** — run recorded validation commands before commit/push
- **Commit Message Format** — `feat(scope-slug): summary`; never use internal change folder names alone as the only message
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — grilling + brainstorming required
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — create artifacts only via OpenSpec CLI/`/opsx-*`
- **OpenSpec Artifact Completeness Rule** — all required change artifacts present
- **Full Plan Depth Rule** — proposal → specs → design → tasks before execution
- **Milestone Commit Cadence** — single commit per change after verification
- **Plan-Doc Embed Rule** — embed guardrails in `proposal.md`/`design.md` and summarize at top of `tasks.md`

## Open Questions

None — the fixture fully specifies product behavior. Scope is fully specified — no ambiguity to interrogate. Remaining technical choices are captured as Decisions above.
