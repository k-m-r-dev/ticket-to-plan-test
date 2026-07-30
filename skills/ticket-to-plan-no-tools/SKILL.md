---
name: ticket-to-plan-no-tools
description: ticket-to-plan process without GSD MCP or OpenSpec. Same ambiguity gates, Required Milestone Map, task depth, and human approval — but hand-authors markdown plan files under the active benchmark run artifacts directory (or docs/plans/ when not benchmarking).
---

# Ticket to Plan (No External Planning Tools)

Same process as `ticket-to-plan-gsd`, without GSD workflow MCP or OpenSpec. Persist plans as plain markdown only.

## Terminology

Use **milestone** / **slice** / **task** as document headings (M001 / S01 / T01 style ids in the markdown itself). These are document identifiers only — no database.

## When this applies

Any new scope. Prefer this skill for benchmark arm `no-tools` or environments without GSD/OpenSpec.

## Full skill compliance

Run **every** step in order. Partial runs are a stop condition.

## Step 0 — Read context

1. `.gsd/DELIVERY-PROFILE.md` if present (delivery vocabulary)
2. `AGENTS.md` if present
3. If benchmarking: `benchmark/runs/<run_id>/` as the output root

**Output root:**  
- Benchmark: `benchmark/runs/<run_id>/artifacts/`  
- Otherwise: `docs/plans/<scope-slug>/`

**Stop condition:** if delivery profile Required fields are missing/ambiguous and needed for the map, stop and ask.

## Step 0.5 — Verify prerequisite skills

`/grilling` and `/brainstorming` must be invocable. Stop if not.

## Step 1 — Take in the scope

Accept pasted tickets/specs. Locked fixtures are valid input.

## Step 2 — Gate ambiguity skills

- Ambiguous → `/grilling` then `/brainstorming`
- Fully specified → skip grilling; say so explicitly; still require design approval in Step 5

## Step 3 — Determine structure

Full tree before execution:

```text
artifacts/
  ROADMAP.md          # top-level unit + Delivery & Guardrails
  S01-<slug>-PLAN.md  # slice plans with tasks
  S02-...
```

- Single milestone unless scope clearly needs split
- Slices = vertical cuts; each independently verifiable
- **Do not** call `gsd_*` or `openspec` CLIs

**Stop condition:** chat-only outline without these files is incomplete.

## Step 4 — Required Milestone Map

In `ROADMAP.md`, section titled exactly `## Delivery & Guardrails` with a complete table: planning ID, scope slug, workstream (optional), external ticket (optional), integration strategy, integration branch, commit cadence (`milestone` for this skill), review unit, Git/PR checkpoint mode, branch name, execution sequence, validation commands, completion condition, size budget.

## Step 5 — Tasks

Each task: inputs, outputs, validation gate; tests in DoD for code tasks. Present design; **human approval before any implementation**.

## Step 6 — Cite guardrails

In `## Delivery & Guardrails`, cite:

- **Task Handoff Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`) — pause after each task; wait for `do next`
- **Commit Gate** — commit only after verified scope per cadence
- **Remote Mutation Rule** — no push/PR without approval
- **Validation Rule** — run validation commands before commit/push
- **Commit Message Format** — `feat(scope-slug): summary`
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-no-tools/SKILL.md`)
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-no-tools/SKILL.md`)
- **No External Planning Tools Rule** (`skills/ticket-to-plan-no-tools/SKILL.md`) — markdown artifacts only; no GSD MCP / OpenSpec
- **Full Plan Depth Rule** — milestone → slice → task before execution
- **Milestone Commit Cadence** — single commit per milestone
- **Plan-Doc Embed Rule** — copy guardrails into each slice plan

## Stop conditions

Incomplete map, missing depth, missing prerequisite skills, or remote mutation without approval.
