# S2 scoring — quick steps

Two paths: **agent draft + your review** (recommended) or fully manual.

## Recommended: draft + review

1. In **your terminal** (not a Cursor chat):

```bash
python3 benchmark/run_s2_draft.py --keep-going
python3 benchmark/s2_xlsx.py merge-drafts
```

2. Open `benchmark/runs/abp-v1/human_sheets/S2_SCORECARD.xlsx`
3. On **Items**, filter `needs_review` = TRUE → fill those Present cells; clear the flag
4. Spot-check some confident rows (`needs_review` = FALSE)
5. Save, then:

```bash
python3 benchmark/s2_xlsx.py apply
python3 benchmark/human_sheet.py ingest --protocol abp-v1
```

Full detail: [`S2_DRAFT_AGENT.md`](S2_DRAFT_AGENT.md)

## Manual only (no agent)

1. Open `S2_SCORECARD.xlsx` (rebuild with `python3 benchmark/s2_xlsx.py emit` if needed)
2. For each Blind ID on **Runs**, open `plans/<Blind ID>/`
3. Fill **Present**, **depth_ok**, **guardrails_ok**
4. `python3 benchmark/s2_xlsx.py apply` then ingest

## Meanings

| Field | TRUE means |
| --- | --- |
| Present | You can point to text covering that checklist item |
| depth_ok | Real structure (slices/tasks or numbered steps) |
| guardrails_ok | Mentions approval / handoff / no push without approval |

Unsure → FALSE (or leave blank + needs_review if still in draft mode).

## Do not open while scoring

- `mapping_key.json`
- `fixtures/todo-api-ambiguous/ANSWER_KEY.md`
