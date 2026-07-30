# Design summary — Todo HTTP API (native arm, f1, r2)

**Ambiguity:** Fixture f1 is fully specified (locked SPEC). **Grilling skipped** — no product decisions to reopen.

**Clarifying questions (would-have-asked):** None. Stack (Rust, Axum, Tokio, sqlx SQLite), endpoints, validation rules, error envelope, persistence, configuration, and test expectations are all locked in the fixture.

**Approach:** Single Rust crate at `apps/todo-api`. Thin layers: configuration from environment, sqlx pool with migrations on startup, repository for todos, Axum routes for health and CRUD, unified JSON error envelope. Integration tests run in-process via tower/Axum test client against isolated SQLite files.

**Execution shape:** Fifteen ordered implementation steps in `IMPLEMENTATION_PLAN.md` (scaffold → persistence → HTTP handlers → server bind → test harness → full suite → clippy). Test scenarios enumerated in `TEST_PLAN.md`.
