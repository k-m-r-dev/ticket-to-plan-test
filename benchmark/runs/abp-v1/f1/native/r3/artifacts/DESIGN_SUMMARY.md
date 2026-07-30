# Design summary — Todo HTTP API (native arm, f1, r3)

**Ambiguity:** Fixture f1 is fully specified (locked SPEC). **Grilling skipped** — no product decisions to reopen.

**Clarifying questions (would-have-asked):** None. The fixture locks stack (Rust, Axum, Tokio, sqlx SQLite), data model, all five CRUD endpoints plus health, validation rules, error envelope, persistence, configuration, and integration-test expectations.

**Approach:** Single Rust crate at `apps/todo-api` with a thin HTTP layer (Axum routes), a repository over sqlx SQLite, and shared error mapping to the required JSON envelope. Migrations run on startup. Integration tests use in-process HTTP against an isolated temp database per test suite.

**Execution shape:** Three phases — foundation (scaffold, config, db, models), HTTP surface (health + todos CRUD with validation), verification (integration tests + clippy gate) — detailed as ordered steps in `IMPLEMENTATION_PLAN.md` with test cases in `TEST_PLAN.md`.
