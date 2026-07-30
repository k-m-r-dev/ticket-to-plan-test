# S01 — Project foundation (scaffold, persistence, health)

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — no commit at slice complete
- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — wait for `do next` after each task
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo check` per task; full `cargo test` after S03

## Goal

Bootstrap the Rust project with Axum + Tokio + sqlx (SQLite), run migrations on startup, read `DATABASE_URL` / `HOST` / `PORT`, and expose `GET /health`.

## Tasks

### T01 — Initialize Cargo workspace

- **Inputs:** Locked stack — Rust, Axum, Tokio, sqlx (SQLite feature), serde, serde_json, uuid, chrono (or `time` for RFC 3339 UTC)
- **Outputs:** `Cargo.toml`, `src/main.rs`, `src/lib.rs`, module tree (`config`, `db`, `models`, `routes`, `error`)
- **Validation gate:** `cargo check`
- **DoD:** Project compiles; binary entrypoint exists

### T02 — Configuration from environment

- **Inputs:** SPEC server + persistence config
- **Outputs:** `src/config.rs` reading:
  - `DATABASE_URL` (default `sqlite:todos.db`)
  - `HOST` (default `127.0.0.1`)
  - `PORT` (default `8080`)
- **Validation gate:** Unit test or smoke that defaults resolve correctly
- **DoD:** Config struct passed into app builder

### T03 — SQLite schema and sqlx migrations

- **Inputs:** SPEC `Todo` model fields
- **Outputs:**
  - `migrations/001_create_todos.sql` with columns: `id` (TEXT UUID), `title` (TEXT NOT NULL), `completed` (INTEGER/boolean default 0), `created_at` (TEXT RFC 3339), `updated_at` (TEXT RFC 3339)
  - `src/db.rs` — pool creation, `sqlx::migrate!()` on startup
- **Validation gate:** App starts against temp DB; `todos` table present after migration
- **DoD:** Migrations idempotent on restart; concurrent-safe enough for single-process local use

### T04 — Axum server shell + health route

- **Inputs:** Config + router skeleton
- **Outputs:** `src/routes/health.rs` — `GET /health` → `200` JSON `{ "status": "ok" }`; main binds `HOST:PORT`
- **Validation gate:** Manual curl or in-process request returns expected body
- **DoD:** Server listens on configured address; health endpoint registered
