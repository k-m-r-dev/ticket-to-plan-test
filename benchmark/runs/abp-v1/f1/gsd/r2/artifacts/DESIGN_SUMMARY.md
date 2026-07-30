# Design summary — Todo HTTP API (M003)

**Ambiguity:** Scope is fully specified (locked SPEC) — grilling skipped.

**Approach:** Single crate at `apps/todo-api` (Axum + Tokio + sqlx SQLite). Layered modules: config, db/migrations, models, error envelope, todos handlers, app router. In-process tower/axum integration tests; no auth/UI/deploy. Alternatives considered: workspace domain/http split and lib+bin split — rejected as overkill for ~800–1200 LOC locked stack.

**Milestone tree:** M003 `todo-http-api` → S01 scaffold+persistence → S02 CRUD+filter+validation → S03 integration tests+clippy. Commit cadence: **milestone** (one commit after verification). Independent of M001 (r1).

**Plan artifacts:** `.gsd/phases/03-todo-http-api/` (copied into this `artifacts/` folder).
