## Context

See `proposal.md` — Why/What Changes. This is a greenfield service crate (no existing todo-api code in the repo). Constraints are fixed by the locked fixture: Rust + Axum + Tokio + SQLite via `sqlx`, JSON over HTTP, no UI/CLI beyond curl examples.

## Goals / Non-Goals

**Goals:**
- Deliver the full CRUD + filter surface from `specs/todo-api/spec.md` with correct validation, error shape, and persistence semantics.
- Keep the implementation simple enough for a single local process (no multi-instance coordination).

**Non-Goals:**
- Authentication/authorization, multi-tenancy, pagination/sorting, soft deletes, Web/mobile UI, OpenAPI generation, containerized deployment, rate limiting/CORS beyond Axum defaults — all excluded per the locked fixture's "Out of scope" list.

## Decisions

- **Crate layout**: single binary crate (`src/main.rs` + modules `routes.rs`, `handlers.rs`, `models.rs`, `error.rs`, `db.rs`) rather than a workspace with separate lib/bin crates. *Alternative considered*: lib+bin split for testability — rejected as unnecessary ceremony for this scope; `axum::Router` + `tower::ServiceExt::oneshot` in-process tests give equivalent testability without the split.
- **IDs**: `uuid::Uuid` generated server-side with `Uuid::new_v4()`, stored/returned as string. *Alternative*: auto-increment integer — rejected because the fixture specifies "UUID string".
- **Timestamps**: `chrono::DateTime<Utc>` serialized as RFC 3339 via `serde` (`chrono`'s serde feature), matching the fixture's `created_at`/`updated_at` requirement. *Alternative*: `time` crate — either satisfies the constraint; `chrono` chosen for wider ecosystem familiarity with `sqlx`.
- **Validation layer**: hand-written validation functions in `models.rs` (trim + length check for title, explicit parse for `completed` query and PATCH-body-non-empty check) rather than pulling in a validation crate (`validator`, `garde`) — the rule set is small enough that a dependency would add more weight than value.
- **Error handling**: a single `AppError` enum implementing `axum::response::IntoResponse`, mapping each variant to `(StatusCode, ErrorBody)` with `code` in `{validation_error, not_found, internal_error}`. *Alternative*: per-handler ad hoc `(StatusCode, Json<...>)` — rejected for consistency risk across 5 handlers.
- **Persistence**: `sqlx::SqlitePool` with compile-time-checked or runtime queries against a single `todos` table; migrations via `sqlx::migrate!` embedded at build time, run once at startup before the listener binds. `DATABASE_URL` read via `std::env`, defaulting to `sqlite:todos.db` when unset.
- **Testing approach**: integration tests under `tests/` using `axum::Router` + `tower::ServiceExt::oneshot` (or an in-process `TestServer`/hyper client) against a temporary SQLite file (`sqlite::memory:` or a per-test temp file) so each test run starts from a clean schema.

## Risks / Trade-offs

- [SQLite file-based concurrency under test parallelism] → Mitigation: use `sqlite::memory:` per test connection or a uniquely-named temp file per test to avoid cross-test interference; Rust's default parallel test runner otherwise risks flaky locking.
- [`completed` query parsing ambiguity for values other than exact `"true"`/`"false"`] → Mitigation: strict match against `"true"`/`"false"` only; anything else (including `"1"`, `"TRUE"`, empty string) is a `400 validation_error`, per spec.
- [Migration drift between fresh and existing DB files across repeated local runs] → Mitigation: `sqlx::migrate!` is idempotent (tracks applied migrations in its own table), safe to run on every startup.

## Delivery & Guardrails

| Field | Value |
| --- | --- |
| Planning ID / change name | `todo-http-api-abp-f1-r2` |
| Scope slug | `todo-http-api` |
| Workstream | n/a (single change) |
| External ticket ID | none (benchmark fixture, no tracker) |
| Integration strategy | `feature-branch` (per `.gsd/DELIVERY-PROFILE.md`) |
| Integration branch | `main` |
| Commit cadence | `milestone` — single commit after the whole change is verified (this skill's fixed cadence; overrides the repo default `slice` cadence) |
| Review unit | `pr-per-milestone` (per `.gsd/DELIVERY-PROFILE.md`) |
| Git/PR checkpoint mode | `milestone` |
| Branch name | `feat/todo-http-api-abp-f1-r2` |
| Execution sequence | Scaffold crate → migrations/db layer → models/validation/error types → handlers/routes → integration tests → clippy/test pass → single commit |
| Validation commands | `cargo test`; `cargo clippy -- -D warnings` |
| Completion condition | All tasks in `tasks.md` checked, `cargo test` and `cargo clippy -- -D warnings` pass |
| Size budget | Single crate, ~6-8 source files, no more than ~600 LOC excluding tests |

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

None — the fixture fully specifies product behavior; remaining technical choices are captured as Decisions above.
