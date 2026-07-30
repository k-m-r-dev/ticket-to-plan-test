# Design summary — Todo HTTP API (OpenSpec r3)

**Ambiguity:** Scope is fully specified (locked SPEC) — grilling skipped; no clarifying questions needed.

**Approach:** Expand existing `apps/todo-api` skeleton into a full Axum + Tokio + sqlx SQLite service. Modules: config, db/migrations, models, error envelope, todo handlers, health handler, app router. In-process tower/axum integration tests; no auth/UI/deploy.

**Change tree:** `todo-http-api-abp-f1-r3` → S01 scaffold+deps → S02 models/validation/error → S03 persistence → S04 handlers/routing → S05 integration tests → S06 clippy+commit. Commit cadence: **milestone** (one commit after verification).

**Plan artifacts:** `openspec/changes/todo-http-api-abp-f1-r3/` (copied into this `artifacts/` folder).
