# Design summary — Local Todo HTTP API (M007)

**Ambiguity:** Ticket intentionally incomplete — grilling simulated in CLARIFICATIONS.md with assumed answers (Rust/Axum/SQLite, REST /todos, no auth, completed filter, no pagination).

**Approach:** Single crate at `apps/todo-api` (Axum + Tokio + sqlx SQLite). Layered modules: config, db/migrations, models, error envelope, todos handlers, app router. In-process tower/axum integration tests.

**Milestone tree:** M007 `local-todo-http-api` → S01 scaffold+persistence → S02 CRUD+filter+validation → S03 integration tests+clippy. Commit cadence: **milestone** (one commit after verification).

**Brainstorming:** Empty list OK; temp sqlite for tests; last-write-wins concurrency acceptable for local v1.

**Plan artifacts:** `.gsd/phases/07-local-todo-http-api/` (copied into this `artifacts/` folder).

**Approval:** Matrix automation treats human design approval as given for planning artifacts only. Execution requires explicit `do next` per Task Handoff Gate.
