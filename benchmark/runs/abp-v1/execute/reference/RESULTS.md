# Execute-to-score — reference oracle proof

**Date:** 2026-07-30  
**Server:** `apps/todo-api-reference/server.py` (Python SPEC-compatible reference)  
**Oracle:** `fixtures/todo-api/oracle`  
**Result:** **5/5 passed** (see `oracle_results.txt`)

## Note on Rust

F1 SPEC locks Rust+Axum. `apps/todo-api/` is a Cargo skeleton for formal arm implements when `cargo` is available. This reference run proves the **locked oracle** works end-to-end (R4 infrastructure).

## Formal arm executes (gsd / openspec / no-tools / native)

**Status:** PENDING — require (1) completed S2 scores on F1 n=3 matrix, (2) median plan selection, (3) Rust toolchain or approved reference language deviation recorded in PROTOCOL amendment.
