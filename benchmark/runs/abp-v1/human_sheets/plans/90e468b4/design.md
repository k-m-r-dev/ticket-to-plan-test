## Context

Greenfield Rust HTTP service for the locked Todo API fixture. See `proposal.md` for motivation and `specs/todo-api/spec.md` for behavioral requirements. Stack is fixed: Axum, Tokio, SQLite via sqlx, JSON over HTTP. No existing application code is assumed for this change.

## Goals / Non-Goals

**Goals:**

- Single-crate Axum service with clear module boundaries (config, db, models, errors, todos handlers, router)
- sqlx migrations applied on startup; env-driven bind and database URL
- In-process tower/axum service tests (no mandatory external process)
- Plan depth sufficient for apply agents: scaffold → CRUD → tests/clippy

**Non-Goals:**

- Auth, multi-user, pagination, soft deletes, UI, or deployment packaging
- Multi-instance SQLite locking beyond single-process local use
- Per-task commits (milestone cadence only)

## Decisions

### D1 — Crate layout at `apps/todo-api`

- **Choice:** One binary crate under `apps/todo-api` with modules `config`, `db`, `error`, `models`, `todos`, `app`.
- **Why:** Matches fixture stack and keeps the surface small for a CRUD API.
- **Alternatives:** Workspace of many crates (overkill); root-level crate only (harder to coexist with benchmark apps).

### D2 — Persistence: sqlx + SQLite migrations

- **Choice:** `sqlx` with compile-time or runtime queries and a `migrations/` folder run at startup.
- **Why:** Locked SPEC requires sqlx migrations and `DATABASE_URL`.
- **Alternatives:** Diesel (out of stack); raw `rusqlite` without migrations (violates SPEC).

### D3 — IDs and timestamps

- **Choice:** UUID v4 strings for `id`; store timestamps as UTC text/datetime compatible with RFC 3339 serialization via chrono (or `time`).
- **Why:** Matches SPEC field types; simple JSON mapping.
- **Alternatives:** Integer PKs (SPEC requires UUID string); client-supplied ids (SPEC says server-generated).

### D4 — Error handling

- **Choice:** Central `AppError` → Axum `IntoResponse` emitting the locked `{ error: { code, message } }` envelope; map validation / not-found / internal explicitly.
- **Why:** Single place to enforce required codes and shape.
- **Alternatives:** Ad-hoc JSON in each handler (drift risk).

### D5 — Testing strategy

- **Choice:** Build the Axum `Router` with a temp SQLite file (or `:memory:` if migration story allows) and issue requests via `tower::ServiceExt` / axum test helpers.
- **Why:** SPEC prefers in-process HTTP tests; deterministic and CI-friendly.
- **Alternatives:** Spin real TCP listener per test (slower, flakier).

### D6 — Commit / delivery

- **Choice:** Feature branch `feature/todo-http-api`, PR per milestone, **milestone** commit cadence (skill override of `.gsd/DELIVERY-PROFILE.md` `slice`).
- **Why:** Ticket-to-plan-openspec requires single commit after verified change.
- **Alternatives:** Slice commits per profile (rejected by this skill’s commit cadence rule).

## Risks / Trade-offs

- **[Risk] sqlx offline/online query mode friction** → Prefer runtime queries or check-in offline data early; keep migrations simple.
- **[Risk] Title trim semantics edge cases** → Document trim-then-validate in handlers; cover whitespace and overlong in tests.
- **[Risk] Scope creep beyond locked SPEC** → Keep tasks limited to HTTP CRUD, persistence, and required tests.
- **[Trade-off] Single-process SQLite** → Adequate for fixture; not multi-writer HA.

## Migration Plan

N/A for greenfield local API. Rollback = delete branch / drop local DB file. No production cutover.

## Open Questions

None — locked SPEC; grilling skipped.
