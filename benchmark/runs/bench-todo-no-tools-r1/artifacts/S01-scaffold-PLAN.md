# S01 — Scaffold + persistence

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — no commit at slice complete
- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — wait for `do next`
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — `cargo test`; `cargo clippy -- -D warnings`

## Goal

Cargo Axum project, sqlx SQLite migrations, HOST/PORT/DATABASE_URL, GET /health.

## Tasks

### T01 Scaffold Cargo Axum project
- Inputs: SPEC stack
- Outputs: `Cargo.toml`, `src/main.rs`
- Validation: `cargo check`
- DoD: deps include axum, tokio, sqlx, serde, uuid

### T02 sqlx todos migration
- Inputs: SPEC data model (id, title, completed, created_at, updated_at)
- Outputs: `migrations/`, `src/db.rs`
- Validation: migrate on startup against temp DB

### T03 Config + health
- Inputs: SPEC server section
- Outputs: wired env + `GET /health` → 200 `{ "status": "ok" }`
- Validation: health responds
