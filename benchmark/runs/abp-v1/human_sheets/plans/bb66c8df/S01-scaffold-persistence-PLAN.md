# S01 — Scaffold + persistence

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — no commit at slice complete
- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — wait for `do next` after each task
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo check` per task; full `cargo test` after S03

## Goal

Establish Cargo project with Axum + Tokio + sqlx (SQLite), apply migrations on startup, wire `HOST` / `PORT` / `DATABASE_URL`, expose `GET /health`.

## Tasks

### T01 — Cargo project scaffold

- **Inputs:** Assumed stack — Rust, Axum, Tokio, sqlx, serde, uuid, chrono (or `time` for RFC 3339)
- **Outputs:** `Cargo.toml`, `src/main.rs`, `src/lib.rs` (optional), module layout (`routes/`, `db/`, `models/`, `error/`)
- **Validation gate:** `cargo check`
- **DoD:** Dependencies resolve; binary compiles; `cargo run` starts server skeleton

### T02 — sqlx SQLite schema + migrations

- **Inputs:** Assumed data model — `id` (UUID text), `title` (text), `completed` (boolean default false), `created_at` / `updated_at` (RFC 3339 UTC)
- **Outputs:** `migrations/001_create_todos.sql`, `src/db.rs` with pool init + `sqlx::migrate!()` on startup
- **Validation gate:** App starts against temp DB file; `todos` table exists after restart (persistence check)
- **DoD:** `DATABASE_URL` env (default `sqlite:todos.db`) drives connection; migrations idempotent on restart

### T03 — Server config + health endpoint

- **Inputs:** Assumed server config — `HOST` default `127.0.0.1`, `PORT` default `8080`
- **Outputs:** Config module reading env vars; Axum router with `GET /health` → `200` `{ "status": "ok" }`
- **Validation gate:** In-process test or curl — health returns expected JSON
- **DoD:** Server binds configured host/port; data survives process restart via SQLite file
