# Design summary — Todo HTTP API (OpenSpec)

**Ambiguity:** Scope is fully specified (locked SPEC) — grilling skipped.

**Approach:** Single crate at `apps/todo-api` (Axum + Tokio + sqlx SQLite). Modules: config, db/migrations, models, error envelope, todos handlers, app router. In-process tower/axum integration tests; no auth/UI/deploy.

**Change tree:** `todo-http-api-abp-f1-r1` → S01 scaffold+persistence → S02 CRUD+filter+errors → S03 integration tests+clippy. Commit cadence: **milestone** (one commit after verification).

**Plan artifacts:** `openspec/changes/todo-http-api-abp-f1-r1/` (copied into this `artifacts/` folder).
