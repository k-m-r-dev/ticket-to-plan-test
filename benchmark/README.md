# Benchmark harness

## Legacy (v0 exploratory)

```bash
python3 benchmark/new_run.py --protocol legacy --arm gsd
python3 benchmark/score.py <run_id>
python3 benchmark/report.py
```

## ABP abp-v1 (decision-grade)

See [`docs/benchmark/PROTOCOL.md`](../docs/benchmark/PROTOCOL.md) and [`docs/benchmark/OPERATOR_RUNBOOK.md`](../docs/benchmark/OPERATOR_RUNBOOK.md).

```bash
python3 benchmark/new_run.py --protocol abp-v1 --fixture f1 --arm gsd --replicate 1
python3 benchmark/score.py benchmark/runs/abp-v1/f1/gsd/r1
python3 benchmark/tiktoken_count.py benchmark/runs/abp-v1/f1/gsd/r1
python3 benchmark/validate_runs.py
python3 benchmark/human_sheet.py emit
python3 benchmark/export_jsonl.py
python3 benchmark/report_abp.py
```

Arms: `gsd` | `openspec` | `no-tools` | `native`  
Fixtures: `f1` | `f2`
