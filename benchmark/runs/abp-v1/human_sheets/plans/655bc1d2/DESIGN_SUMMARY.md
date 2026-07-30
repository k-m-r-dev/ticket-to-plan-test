# Design summary — Todo HTTP API (native arm, f1)

**Ambiguity:** Fixture f1 is fully specified (locked SPEC). **Grilling skipped** — no product decisions to reopen.

**Clarifying questions (would-have-asked):** None. Stack (Rust, Axum, Tokio, sqlx SQLite), endpoints, validation rules, error envelope, persistence, configuration, and test expectations are all locked in the fixture.

**Approach:** Single crate at `apps/todo-api`. Layered modules: `config`, `db` (sqlx pool + migrations), `models`, `error`, `routes` (health + todos). In-process Axum/tower integration tests against a temp SQLite file. No auth, UI, or deployment work.

**Execution shape:** Three phases — scaffold + persistence, HTTP surface + validation, integration tests + clippy gate — implemented as ordered steps in `IMPLEMENTATION_PLAN.md` with test coverage in `TEST_PLAN.md`.
