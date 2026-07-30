# Operator runbook (plain English) — ABP abp-v1

This guide tells you **exactly what to do** to finish the real benchmark.  
You do **not** need Cargo/Rust for these planning steps.

**Want an agent to do Step 1 for you?** See [`AGENT_RUNNER.md`](AGENT_RUNNER.md) (one new chat per run; you still do human S2 yourself).

---

## What you are doing (big picture)

You will run **24 separate planning sessions** in Cursor.

Each session:

1. Reads a prompt  
2. Writes a **plan only** (no coding the app)  
3. Saves the plan files into a folder  
4. We score those files later  

There are:

- **2 fixtures** (what to plan): `f1` = full locked SPEC, `f2` = vague ticket  
- **4 arms** (how to plan): `gsd`, `openspec`, `no-tools`, `native`  
- **3 repeats** each (`r1`, `r2`, `r3`)  

2 × 4 × 3 = **24**.

---

## Rules (read once)

1. Use the **same AI model** for all 24 runs.  
2. Start a **brand new Cursor chat** for every run. Do not reuse an old chat.  
3. Stop when the **plan is ready**. Do **not** implement the Todo app in these runs.  
4. For **f2** runs: do **not** open `fixtures/todo-api-ambiguous/ANSWER_KEY.md` while planning. That file is only for scoring later.  
5. When you save results, put plan files **only** in that run’s `artifacts/` folder.

---

## Step 0 — Folders are already created

The 24 folders should already exist under:

`benchmark/runs/abp-v1/`

Example path:

`benchmark/runs/abp-v1/f1/gsd/r1/`

Inside each folder you will see:

- `prompt.md` — what to paste / follow in Cursor  
- `meta.json` — timing and notes (you edit this)  
- `artifacts/` — empty; you put the plan files here  

If a folder is missing, ask the agent to re-run scaffolding, or run:

```bash
python3 benchmark/new_run.py --protocol abp-v1 --fixture f1 --arm gsd --replicate 1
```

(Change `f1` / `gsd` / `1` as needed.)

---

## Step 1 — Do one run (repeat this 24 times)

Pick the next empty slot. Suggested order (keeps tools from mixing):

1. All **f1 + gsd** (`r1`, `r2`, `r3`)  
2. All **f1 + openspec**  
3. All **f1 + no-tools**  
4. All **f1 + native**  
5. Then the same four arms for **f2**

### 1a. Open the prompt

Open:

`benchmark/runs/abp-v1/<fixture>/<arm>/r<n>/prompt.md`

Example: `benchmark/runs/abp-v1/f1/gsd/r1/prompt.md`

### 1b. Mark the start time

Open `meta.json` in the same folder.

Set:

- `"status": "running"`  
- `"started_at": "<current UTC time>"` (example: `"2026-07-30T11:00:00+00:00"`)  
- `"model": "<the model name you are using>"`

Save the file.

### 1c. Start a new Cursor chat

Copy the instructions from `prompt.md` into a **new** chat.

Follow the arm:

| Arm | What to do in plain English |
| --- | --- |
| `gsd` | Use the **ticket-to-plan-gsd** skill and GSD tools to make a full plan |
| `openspec` | Use the **ticket-to-plan-openspec** skill and OpenSpec to make a full plan |
| `no-tools` | Use the **ticket-to-plan-no-tools** skill; write markdown plans yourself (no GSD/OpenSpec) |
| `native` | **No skill** — just ask the AI for a complete implementation plan |

Stop when the plan is complete. Do not build the app.

### 1d. Save the plan files

Copy every plan file the session produced into:

`benchmark/runs/abp-v1/<fixture>/<arm>/r<n>/artifacts/`

Examples of what to copy:

- GSD: ROADMAP / slice PLAN markdown  
- OpenSpec: `proposal.md`, `design.md`, `tasks.md`, specs  
- no-tools / native: whatever plan markdown you got  

### 1e. Mark the end time

Edit `meta.json` again:

- `"ended_at": "<UTC time when plan was finished>"`  
- `"wall_clock_seconds": <seconds from start to end>`  
- `"tool_calls": <how many tool/MCP/CLI calls you roughly used>` (0 is fine for native/no-tools if none)  
- Optional: if Cursor shows token usage, put it under `tokens.cursor_ui`  
- `"status": "plan_ready"`

Save.

### 1f. Auto-score this run

In a terminal, from the project root:

```bash
python3 benchmark/score.py benchmark/runs/abp-v1/<fixture>/<arm>/r<n>
python3 benchmark/tiktoken_count.py benchmark/runs/abp-v1/<fixture>/<arm>/r<n>
```

Example:

```bash
python3 benchmark/score.py benchmark/runs/abp-v1/f1/gsd/r1
python3 benchmark/tiktoken_count.py benchmark/runs/abp-v1/f1/gsd/r1
```

### 1g. Check off and move on

Tick that run on a paper/digital checklist, then start the **next** new chat for the next folder.

---

## Step 2 — After all 24 say `plan_ready`

Run these commands from the project root (one after another):

```bash
python3 benchmark/validate_runs.py --protocol abp-v1
```

You want `"awaiting_operator": 0` and no `"bad"` entries.

Sheets for human scoring were already created. If you need to recreate them:

```bash
python3 benchmark/human_sheet.py emit --protocol abp-v1
```

---

## Step 3 — Human scoring (S2) — the important fair score

**Recommended: agent draft + your review** (saves time; you stay the official scorer).

See [`S2_DRAFT_AGENT.md`](S2_DRAFT_AGENT.md) and [`S2_QUICKSTART.md`](S2_QUICKSTART.md).

```bash
# from YOUR terminal (not from a Cursor chat)
python3 benchmark/run_s2_draft.py --keep-going
python3 benchmark/s2_xlsx.py merge-drafts
# open S2_SCORECARD.xlsx → filter needs_review=TRUE → fix → spot-check
python3 benchmark/s2_xlsx.py apply
python3 benchmark/human_sheet.py ingest --protocol abp-v1
python3 benchmark/export_jsonl.py --protocol abp-v1
python3 benchmark/report_abp.py --protocol abp-v1
python3 benchmark/disagreement_s1_s2.py --protocol abp-v1
```

Workbook: [`benchmark/runs/abp-v1/human_sheets/S2_SCORECARD.xlsx`](../../benchmark/runs/abp-v1/human_sheets/S2_SCORECARD.xlsx)

**Do not open `mapping_key.json` while scoring** (it reveals which arm wrote the plan).  
**Do not open** `fixtures/todo-api-ambiguous/ANSWER_KEY.md` while scoring f2 plans.

Agent drafts are **not** official S2 until you review flagged rows (and spot-check) then apply.

### Manual Excel only

Fill `S2_SCORECARD.xlsx` yourself (no draft agent), then the same `apply` + ingest commands.
---

## Step 4 — Optional: build from a plan (execute-to-score)

Do this **only after** Step 3.

1. For each of the four arms on **f1**, pick the middle-quality plan (median human coverage).  
2. In a clean folder/worktree, implement **only from that plan**.  
3. Start the server.  
4. Run:

```bash
source .venv/bin/activate   # if you use the project venv
ORACLE_BASE_URL=http://127.0.0.1:8080 pytest fixtures/todo-api/oracle -v
```

5. Save the result under `benchmark/runs/abp-v1/execute/<arm>/`.

Rust/Cargo is only needed if you implement as Rust. The planning benchmark itself does **not** need Cargo.

---

## Step 5 — Done when…

- All 24 runs are `plan_ready`  
- Human sheets are filled and ingested  
- `docs/benchmark/ACCEPTANCE_REPORT.md` can be updated with real R1–R4 results  

Until then, the benchmark is **ready to run**, not yet **accepted**.

---

## Quick “one run” cheat sheet

```text
1. New Cursor chat
2. Open prompt.md for that run
3. Edit meta.json → started_at, status=running
4. Plan only (follow the arm)
5. Copy plans → artifacts/
6. Edit meta.json → ended_at, wall_clock_seconds, tool_calls, status=plan_ready
7. Run score.py + tiktoken_count.py
8. Next run
```
