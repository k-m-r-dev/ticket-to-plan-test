# Design summary — Todo HTTP API (M004)

**Ambiguity:** Scope is fully specified (locked SPEC) — grilling skipped. Brainstorming noted: isolate SQLite per test (temp/:memory:), trim titles, empty PATCH vs missing fields, keep OpenAPI/Docker OOS.

**Approach:** Single crate at `apps/todo-api` (Axum + Tokio + sqlx SQLite). Layered modules: config, db/migrations, models, error envelope, todos handlers, app router. In-process tower/axum integration tests; no auth/UI/deploy.

**Milestone tree:** M004 `todo-http-api` → S01 scaffold+persistence → S02 CRUD+filter+validation → S03 integration tests+clippy. Commit cadence: **milestone** (one commit after verification).

**Plan artifacts:** `.gsd/phases/04-todo-http-api/` (copied into this `artifacts/` folder).
