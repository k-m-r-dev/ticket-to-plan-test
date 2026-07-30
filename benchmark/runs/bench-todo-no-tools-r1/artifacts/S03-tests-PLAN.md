# S03 — Integration tests + polish

## Delivery & Guardrails (embedded)

- Commit cadence: **milestone** — single commit after M001 verified
- **Task Handoff Gate** — wait for `do next`

## Goal

Full SPEC test coverage and clippy clean.

## Tasks

### T01 Integration suite
- Cover CRUD, filter, validation, 404
- Validation: `cargo test`

### T02 Clippy
- Validation: `cargo clippy -- -D warnings`

## Stop

Human approval before any implementation.
