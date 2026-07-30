# DeepEval acceptance package (S3)

```bash
cd benchmark/acceptance
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...   # or provider key DeepEval needs
pytest -q
```

Without API keys, tests **skip** (S1+S2 remain acceptance blockers per PROTOCOL).

Full-matrix scoring: load `../runs/abp-v1/export.jsonl` and write per-run `score_s3.json` (extend this package as runs complete).
