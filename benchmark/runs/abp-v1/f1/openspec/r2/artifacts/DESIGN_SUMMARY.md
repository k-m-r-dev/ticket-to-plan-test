# Design summary — Todo HTTP API (OpenSpec)

**Ambiguity:** Scope is fully specified by the locked benchmark fixture (`fixtures/todo-api/SPEC.md`) — no product ambiguity to interrogate; grilling and brainstorming skipped.

**Approach:** Single Rust binary crate (Axum + Tokio + sqlx SQLite). Modules: `config`, `db` (migrations + repository), `models`, `error`, `handlers`, `routes`, `main`. Server-generated UUID ids, RFC 3339 timestamps via `chrono`, shared `AppError` mapping to the required `{ "error": { "code", "message" } }` envelope. In-process `tower`/`axum` integration tests against per-test SQLite (`memory` or temp file).

**Change:** `todo-http-api-abp-f1-r2` — seven task groups (scaffold → model/error types → validation → persistence → HTTP handlers → integration tests → final verification). Commit cadence: **milestone** (one commit after `cargo test` and `cargo clippy -- -D warnings` pass).

**Clarifying questions (none required):** Fixture is locked; no assumptions beyond documented technical decisions in `design.md`.

**Plan artifacts:** `openspec/changes/todo-http-api-abp-f1-r2/` (copied into this `artifacts/` folder).
