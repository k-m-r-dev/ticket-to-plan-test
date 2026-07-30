# S2 human scoring status

- Sheets emitted: 24 (`benchmark/runs/abp-v1/human_sheets/*.json`)
- Mapping key: `human_sheets/mapping_key.json` (**scorers must not open while scoring**)
- Ingested complete sheets: **0**

Fill each sheet (`present`: true/false, `depth_ok`, `guardrails_ok`), then:

```bash
python3 benchmark/human_sheet.py ingest --protocol abp-v1
python3 benchmark/disagreement_s1_s2.py --protocol abp-v1
```
