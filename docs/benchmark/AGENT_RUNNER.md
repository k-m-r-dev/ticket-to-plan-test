# ABP Matrix Runner Agent — how to use

## Two ways to drive the matrix

- **Unattended** — `benchmark/run_matrix.py` launches one headless `cursor-agent` session per slot, back to back. Start it once and walk away.
- **Interactive** — open a new Cursor chat per slot and invoke the skill by hand.

Both paths use the same skill and produce identical artifacts. The driver is preferred: a separate process per slot enforces run isolation more strictly than remembering to open a new chat.

## What it is

A Cursor skill that performs **one** planning benchmark run from the operator runbook:

- picks the next `awaiting_operator` slot
- runs the correct planning arm
- saves plans into `artifacts/`
- scores with S1 + TikToken

It does **not** do human S2 scoring and does **not** build the app.

## Unattended driver

Requires the Cursor CLI (`cursor-agent`) on `PATH` and an authenticated Cursor session.

**Run it from your own terminal, not from inside a Cursor chat.** A driver launched by an agent tool call is killed when that tool call ends — `nohup` and `disown` do not save it, and its in-flight `cursor-agent` children die with it (SIGKILL, empty logs). Started from a normal terminal the driver owns its own lifecycle and runs to completion.

```bash
python3 benchmark/run_matrix.py --list                  # what is queued, no execution
python3 benchmark/run_matrix.py --dry-run --max-runs 1  # show the exact CLI call
python3 benchmark/run_matrix.py --max-runs 1            # prove one slot end to end
python3 benchmark/run_matrix.py                         # drain the queue
```

| Flag | Default | Purpose |
| --- | --- | --- |
| `--model` | `composer-2.5` | Pinned model for every arm. Changing it mid-matrix breaks cross-arm comparability. |
| `--max-runs` | `24` | Safety cap on slots per invocation. |
| `--timeout` | `2400` | Per-run seconds before the session is killed and the slot released. |
| `--keep-going` | off | Continue after a failed slot instead of stopping. |
| `--retry-stalled` | off | Also pick up slots stuck in `running` from a crashed session. |
| `--sandbox` | inherit | Pass `disabled` if a run fails on tool permissions. |

Each session runs with `--force --trust --approve-mcps` so it never blocks on an approval prompt. Logs land in `benchmark/runs/abp-v1/_driver_logs/<fixture>-<arm>-<rN>.log`.

### Failure handling

A slot only counts as done when `status` reaches `plan_ready`/`scored` **and** `artifacts/` is non-empty. Otherwise the driver releases it back to `awaiting_operator`, records `driver_last_error` in `meta.json`, and stops (or continues with `--keep-going`). Re-running the driver retries released slots, so a crash never loses a slot and never silently produces an empty run.

### Two wall-clock numbers

`meta.json` carries both:

- `wall_clock_seconds` — agent-reported planning time.
- `driver_wall_seconds` — full process time, including CLI startup and the scoring commands.

`driver_wall_seconds` is the more reproducible of the two because nothing self-reports it. Pick one definition before writing up results and use it consistently.

### Non-interactive effect on F2

The F2 ticket asks the planner to clarify first, and a headless session has nobody to ask. The driver instructs it to write the questions it would have asked plus the answer it assumed into the artifacts. All four arms get that same instruction, so arm-vs-arm comparison holds — but F2 numbers are not comparable to an interactive session where a human answers.

## Interactive path

1. Open a **new Cursor chat** in this repo.
2. Say something like:

> Run the next ABP matrix slot using the abp-matrix-runner skill.

3. Wait until it reports `plan_ready`.
4. Open **another new chat** and repeat until `next_run.py` says nothing is left.

Why new chats? So runs stay independent (less leaked context between arms).

## Helpers

```bash
python3 benchmark/next_run.py --json          # show next slot
python3 benchmark/mark_run.py <dir> start --model "..."
python3 benchmark/mark_run.py <dir> finish --tool-calls N
python3 benchmark/validate_runs.py --protocol abp-v1
```

Order matters when scoring by hand: `tiktoken_count.py` must run **before** `score.py`, because `score.py` copies token counts out of `meta.json`.

## After 24 plan_ready

You (human) still do S2 blind sheets — see [`OPERATOR_RUNBOOK.md`](OPERATOR_RUNBOOK.md) Step 3. The driver never touches `human_sheets/`.
