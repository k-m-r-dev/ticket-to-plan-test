# S01 — Scaffold, persistence, and health

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — no slice-level commit
- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — wait for `do next` after each task
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo check` per task; full `cargo test` after S03

## Goal

Create Cargo project (Rust + Axum + Tokio + sqlx), apply SQLite migrations on startup, read `DATABASE_URL` / `HOST` / `PORT`, expose `GET /health`.

## Tasks

### T01 — Cargo workspace scaffold

- **Inputs:** Assumed stack — Rust, axum, tokio, sqlx (sqlite), serde, serde_json, uuid, chrono (RFC 3339)
- **Outputs:** `Cargo.toml`, `src/main.rs`, modules: `config`, `db`, `routes`, `models`, `error`
- **Validation gate:** `cargo check`
- **DoD:** Binary compiles; `cargo run` starts listener skeleton

### T02 — Configuration from environment

- **Inputs:** Defaults — `DATABASE_URL=sqlite:todos.db`, `HOST=127.0.0.1`, `PORT=8080`
- **Outputs:** `config.rs` parsing env vars with fallbacks; log effective bind address at startup
- **Validation gate:** Unit test or manual run confirms overrides work
- **DoD:** Server binds configured host/port; localhost-only default satisfies local-use constraint

### T03 — sqlx SQLite pool + migrations

- **Inputs:** Schema — `todos(id TEXT PK, title TEXT NOT NULL, completed BOOLEAN DEFAULT 0, created_at TEXT, updated_at TEXT)`
- **Outputs:** `migrations/001_create_todos.sql`, `db.rs` with pool init and `sqlx::migrate!()` before serving
- **Validation gate:** Start app twice against same file — table exists; rows persist across restart
- **DoD:** Migration runs idempotently on every startup

### T04 — Health route

- **Inputs:** Axum router
- **Outputs:** `GET /health` → `200` JSON `{ "status": "ok" }`
- **Validation gate:** In-process test or curl against running server
- **DoD:** Health responds without DB dependency failure masking readiness
