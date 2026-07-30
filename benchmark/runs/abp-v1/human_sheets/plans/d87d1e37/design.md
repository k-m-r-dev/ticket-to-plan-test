## Context

Greenfield Rust HTTP service for the ambiguous Todo ticket. Open questions from the ticket (stack, routes, errors, filter, auth) were resolved via documented grilling assumptions (see run `artifacts/CLARIFICATIONS.md`). Behavioral requirements live in `specs/todo-api/spec.md`. No existing application code is assumed.

## Goals / Non-Goals

**Goals:**

- Single-crate Axum service with clear modules: config, db, models, errors, todos handlers, router
- sqlx migrations on startup; env-driven bind and database URL
- In-process tower/axum integration tests with temp SQLite
- Plan depth: scaffold → CRUD → tests/clippy

**Non-Goals:**

- Auth, multi-user tenancy, pagination, sorting, UI, OpenAPI artifact, Docker/K8s deploy
- GraphQL/gRPC, rate limiting, CORS policy beyond defaults
- Soft deletes; multi-instance SQLite beyond single-process local use
- Per-task commits (milestone cadence only)

## Decisions

### D1 — Stack: Rust + Axum + Tokio + SQLite/sqlx

- **Choice:** Rust binary with Axum on Tokio; SQLite via sqlx with `migrations/` applied at startup.
- **Why:** Small typed service, one-command `cargo run`, file persistence without a DB server — matches team “keep it simple / local” constraint.
- **Alternatives:** Node/Express (less alignment with benchmark primary fixture); Postgres (extra ops for local use).

### D2 — Crate layout at `apps/todo-api`

- **Choice:** One binary crate under `apps/todo-api` with modules `config`, `db`, `error`, `models`, `todos`, `app`.
- **Why:** Keeps surface small; coexists with other benchmark apps.
- **Alternatives:** Workspace of many crates (overkill for CRUD).

### D3 — API routes and status codes

- **Choice:** `POST /todos` (201), `GET /todos` (200), `GET /todos/:id` (200/404), `PATCH /todos/:id` (200/400/404), `DELETE /todos/:id` (204/404), `GET /health` (200).
- **Why:** RESTful CRUD with explicit codes from grilling assumptions.
- **Alternatives:** `/api/v1/todos` prefix (unnecessary for local v1).

### D4 — Error envelope

- **Choice:** Central `AppError` → `{ "error": { "code", "message" } }` with codes `validation_error`, `not_found`, `internal_error`.
- **Why:** Consistent client + test assertions; ticket left shape open.
- **Alternatives:** Plain-text errors (poor for JSON API).

### D5 — Filtering: completed only, no pagination

- **Choice:** `GET /todos?completed=true|false`; invalid values → 400 `validation_error`; no page/limit/sort.
- **Why:** Ticket asked about filtering; pagination deferred.
- **Alternatives:** Full query DSL (overplanning for v1).

### D6 — Auth: none

- **Choice:** No auth middleware or tokens; document local single-user assumption.
- **Why:** Ticket lists auth as open; local use constraint in ticket.
- **Alternatives:** API key header (out of scope v1).

### D7 — IDs, timestamps, validation

- **Choice:** UUID v4 string `id`; RFC 3339 UTC timestamps; trim title then enforce length 1..=200; PATCH requires ≥1 field.
- **Why:** Standard CRUD semantics; clear validation_error paths for tests.

### D8 — Config

- **Choice:** `DATABASE_URL` default `sqlite:todos.db`, `HOST` default `127.0.0.1`, `PORT` default `8080`.
- **Why:** Env overrides without extra config files; one-command run.

### D9 — Testing strategy

- **Choice:** Build Axum `Router` with temp SQLite file; exercise HTTP via tower/axum test helpers.
- **Why:** Deterministic CI; no separate test DB server.

### D10 — Commit / delivery

- **Choice:** Feature branch `feature/todo-http-api`, PR per milestone, **milestone** commit cadence (skill override of profile `slice`).
- **Why:** ticket-to-plan-openspec requires single commit after verified change.

## Risks / Trade-offs

- **[Risk] sqlx query/migration friction** → Keep migrations minimal; validate early with temp DB in tests.
- **[Risk] Title trim edge cases** → Cover whitespace and overlong in integration tests.
- **[Risk] Scope creep (auth, pagination, OpenAPI)** → Explicit non-goals in spec and clarifications.
- **[Trade-off] Single-process SQLite** → Adequate for local v1; not multi-writer HA.
- **[Trade-off] Last-write-wins PATCH** → Acceptable for single-user local use.

## Migration Plan

N/A greenfield. Rollback = delete branch / remove local sqlite file.

## Open Questions (resolved via assumed answers)

All ticket open questions were resolved non-interactively; full Q&A tables in run `artifacts/CLARIFICATIONS.md`. Summary:

| Area | Resolution |
| --- | --- |
| Language / framework | Rust, Axum, Tokio |
| Database | SQLite via sqlx migrations |
| URL paths / status codes | `/todos` CRUD + `/health`; 201/200/204/400/404 |
| Error JSON | `{ error: { code, message } }` |
| Filtering | `completed=true\|false` only; no pagination |
| Auth | None (out of scope) |

Brainstorming gaps addressed: empty list returns `[]`; restart persistence via sqlite file; `/health` for liveness only; DELETE missing → 404.
