# S01 — Workspace & persistence foundation

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — no commit at slice complete
- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — wait for `do next` after each task
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo check` per task; full `cargo test` after S03

## Goal

Create the Cargo project, wire environment configuration, apply sqlx SQLite migrations on startup, and register `GET /health`.

## Tasks

### T01 — Cargo workspace and dependency graph

- **Inputs:** Locked stack — Rust, Axum, Tokio, sqlx (SQLite), serde, serde_json, uuid, chrono (RFC 3339 UTC)
- **Outputs:** `Cargo.toml`, `src/main.rs`, `src/lib.rs`, modules: `config`, `db`, `models`, `routes`, `error`
- **Validation gate:** `cargo check`
- **DoD:** Binary compiles; library exposes `app::build_router()` (or equivalent factory) for tests

### T02 — Environment configuration

- **Inputs:** SPEC persistence + server defaults
- **Outputs:** `src/config.rs` loading:
  - `DATABASE_URL` (default `sqlite:todos.db`)
  - `HOST` (default `127.0.0.1`)
  - `PORT` (default `8080`)
- **Validation gate:** Unit test asserting defaults and env override behavior
- **DoD:** `Config` injected into app bootstrap

### T03 — SQLite schema and migration runner

- **Inputs:** SPEC `Todo` fields
- **Outputs:**
  - `migrations/001_create_todos.sql` — `id` TEXT (UUID), `title` TEXT NOT NULL, `completed` INTEGER default 0, `created_at` / `updated_at` TEXT (RFC 3339)
  - `src/db.rs` — connection pool, `sqlx::migrate!()` before serving traffic
- **Validation gate:** Startup against temp file DB; `todos` table exists
- **DoD:** Restart is idempotent; safe for single-process local concurrency (no multi-instance requirement)

### T04 — Axum server bootstrap and health route

- **Inputs:** `Config`, db pool handle
- **Outputs:** `src/routes/health.rs` — `GET /health` → `200` `{ "status": "ok" }`; `main` binds `HOST:PORT`
- **Validation gate:** In-process request or curl returns expected JSON
- **DoD:** Server listens on configured address; router ready for `/todos` routes in S02
