# S2 draft agent + review queue

Agent drafts scores. **You** remain the official scorer for flagged rows and spot-checks.

## Flow

```text
run_s2_draft.py  →  drafts/<blind_id>.json
        ↓
s2_xlsx.py merge-drafts  →  S2_SCORECARD.xlsx (Present filled OR needs_review=TRUE)
        ↓
You: filter needs_review=TRUE, fill blanks, spot-check some confident rows
        ↓
s2_xlsx.py apply  →  human_sheets/*.json
        ↓
human_sheet.py ingest  →  official S2 summary
```

## Run the draft agent (your terminal)

Do **not** launch this from a Cursor chat — the driver can be killed when the tool call ends.

```bash
cd /Users/khandkermahmudur/Workspace/openspec-test
python3 benchmark/run_s2_draft.py --list                 # what’s pending
python3 benchmark/run_s2_draft.py --max-runs 1           # smoke one Blind ID
python3 benchmark/run_s2_draft.py --keep-going           # all 24
```

The terminal streams concise Cursor Agent activity, prints a heartbeat every
15 seconds when no event arrives, announces when the draft file appears, and
ends with a confidence/review summary. Full JSON event logs are kept under
`human_sheets/_s2_draft_logs/<blind_id>.log`.

The pre-launch wait only watches other `--print` sessions (not the always-on
Cursor agent worker), so you should not see a ~2 minute idle pause every run.

Then:

```bash
python3 benchmark/s2_xlsx.py merge-drafts
open benchmark/runs/abp-v1/human_sheets/S2_SCORECARD.xlsx
```

## How you review

1. Open **Items** → filter `needs_review` = TRUE (amber queue).
2. Open the plan folder on **Runs** for that Blind ID.
3. Set **Present** TRUE/FALSE; set `needs_review` = FALSE when done.
4. Same for **Runs** `depth_needs_review` / `guardrails_needs_review`.
5. Spot-check a sample of rows where `needs_review` = FALSE (agent was confident).
6. Save → apply → ingest:

```bash
python3 benchmark/s2_xlsx.py apply
python3 benchmark/human_sheet.py ingest --protocol abp-v1
```

## Blindness

- Plans live at `human_sheets/plans/<Blind ID>/` as **opaque copies** (no arm name in the path).
- Agent skill forbids `mapping_key.json`, `ANSWER_KEY.md`, and arm-named run paths.

## What is official

| Layer | Role |
| --- | --- |
| S1 (`score.py`) | Automated rubric (supporting) |
| Agent draft | Review queue helper — **not** acceptance S2 |
| S2 after your apply + ingest | **Primary** human-confirmed score |

## Files

| Path | Purpose |
| --- | --- |
| `.cursor/skills/abp-s2-draft/SKILL.md` | One Blind ID draft skill |
| `benchmark/run_s2_draft.py` | Headless cursor-agent driver |
| `benchmark/s2_xlsx.py` | emit / merge-drafts / apply / status |
| `human_sheets/drafts/` | Per–Blind ID draft JSON |
| `human_sheets/S2_SCORECARD.xlsx` | Your review UI |
