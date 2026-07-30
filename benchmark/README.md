# Benchmark harness

## Quick start

```bash
python3 benchmark/new_run.py --arm gsd
# run Cursor planning session using the printed run dir's prompt.md
# copy plan artifacts into benchmark/runs/<run_id>/artifacts/
# edit meta.json: started_at, ended_at, wall_clock_seconds, tokens, tool_calls

python3 benchmark/score.py <run_id>
python3 benchmark/report.py
python3 benchmark/report.py --csv benchmark/runs/comparison.csv
```

Arms: `gsd` | `openspec` | `no-tools` | `native`

OpenSpec CLI (local): `npx openspec --version`
