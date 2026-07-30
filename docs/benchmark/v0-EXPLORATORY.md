# v0 Exploratory runs (NOT decision-grade)

The runs under [`benchmark/runs/bench-todo-*-r1`](../../benchmark/runs/) were produced to **prove the harness pipeline**, not to support adoption decisions.

## Why exploratory

- n=1  
- Not four independent operator Cursor sessions  
- Wall-clock and tokens estimated (`estimate_chars`)  
- Keyword scoring only (no blind human S2, no DeepEval S3)  
- No execute-to-score against a locked oracle  

## Decision-grade study

Use **Acceptance Benchmark Protocol `abp-v1`**:

- [`PROTOCOL.md`](PROTOCOL.md)  
- Runs under `benchmark/runs/abp-v1/`  
- Report: [`ACCEPTANCE_REPORT.md`](ACCEPTANCE_REPORT.md)  

Do not cite v0 COMPARISON.md as undoubtable evidence in team decisions.
