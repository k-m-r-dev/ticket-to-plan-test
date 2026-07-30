---
name: ticket-to-plan-openspec
description: OpenSpec thin adapter of ticket-to-plan. Same steps and gates as the GSD skill, but persists plans as OpenSpec change artifacts (proposal, specs, design, tasks) via openspec CLI /opsx commands instead of GSD workflow MCP. Stops for human approval before execution.
---

# Ticket to Plan (OpenSpec)

Thin adapter of `ticket-to-plan-gsd`. Keep every step in order. Swap only the planning backend: OpenSpec change artifacts instead of GSD MCP / `.gsd` trees.

See `skills/MAPPING.md` for GSD ↔ OpenSpec term mapping.

## Terminology

**Change** = OpenSpec top-level planning unit (maps from GSD milestone/phase).  
**Tasks checklist** in `tasks.md` = slices + tasks depth (group tasks under slice-like headings when useful).  
DB-style IDs (`M001`) are not used; use the kebab-case **change name** as the stable id.

## When this applies

Same as GSD skill: any new piece of scope (ticketed or not). External tickets optional.

## Full skill compliance

Run **every** step in order. Partial runs are a stop condition — restart from Step 0.

## Step 0 — Read workflow / project context, in order

1. `openspec/config.yaml` — schema and project context
2. `skills/MAPPING.md` — term mapping for this adapter
3. `.gsd/DELIVERY-PROFILE.md` — if present, reuse integration strategy / branch / review unit vocabulary for the Delivery & Guardrails table (OpenSpec does not replace delivery policy)
4. `AGENTS.md` — if present

**Stop condition:** if delivery fields needed for the Required Map cannot be filled from `.gsd/DELIVERY-PROFILE.md` or explicit user input, stop and ask. Do not invent an integration strategy.

## Step 0.5 — Verify prerequisite skills are invocable

Confirm `/grilling` and `/brainstorming` are available.

**Stop condition:** if either is missing, stop immediately. Do not create OpenSpec artifacts until both are available.

## Step 1 — Take in the scope

Accept ticket text, pasted spec, or tracker fetch. Locked benchmark fixtures count as fully specified input.

## Step 2 — Gate ambiguity-resolution skills on actual ambiguity

- **If ambiguous:** run `/grilling` one question at a time; then `/brainstorming` for structural gaps.
- **If fully specified:** skip grilling and say so explicitly ("scope is fully specified — no ambiguity to interrogate"). Still present design for approval in Step 5.

## Step 3 — Determine change / task structure

Apply Full Upfront Planning Rule: **proposal + specs + design + tasks** must exist before execution. Chat-only outlines are a stop condition.

- Prefer a single OpenSpec change unless scope is clearly multi-change.
- Inside `tasks.md`, use numbered groups (slices) each with checkboxed tasks that are independently verifiable.

### OpenSpec planning artifacts

Create and persist plan artifacts **via OpenSpec**:

```bash
npx openspec new change "<kebab-name>"
npx openspec status --change "<kebab-name>" --json
npx openspec instructions <artifact-id> --change "<kebab-name>" --json
```

Or follow `/opsx-propose` / Cursor OpenSpec skills so that `openspec/changes/<name>/` contains:

- `proposal.md`
- `specs/**/spec.md`
- `design.md`
- `tasks.md`

**Stop condition:** if OpenSpec CLI is unavailable and Cursor OpenSpec commands cannot be used, stop and ask — do not invent a parallel tree outside `openspec/changes/`.

### Artifact completeness

Create **all** artifacts in the schema’s required set (spec-driven: proposal, specs, design, tasks). Do not stop after `tasks.md` alone if dependencies are missing.

## Step 4 — Fill the Required Milestone Map completely

Add a section titled exactly `## Delivery & Guardrails` to `proposal.md` (or `design.md` if proposal is too short) containing every field as a table:

top-level-unit/planning ID (use change name), human-readable scope slug, workstream name (if multi-change), external ticket ID (optional), integration strategy, integration branch, commit cadence, review unit, Git/PR checkpoint mode, branch name (if applicable), execution sequence, validation commands, completion condition, size budget.

**Commit cadence (this skill):** `milestone` (single commit after the whole change is verified) — state this in `tasks.md` so apply agents do not commit per checkbox.

Pull delivery defaults from `.gsd/DELIVERY-PROFILE.md` when present; record deviations.

## Step 5 — Break work into tasks

Each task in `tasks.md` needs inputs, outputs, and a validation gate. Code-changing tasks include tests in their definition of done.

Present the design briefly and get **explicit human approval** before `/opsx-apply` or any implementation.

## Step 6 — Cite guardrails, don't restate them

In `## Delivery & Guardrails`, add Guardrails entries in the form **Rule name** (`source file`) — one-line description:

- **Task Handoff Gate** (`.gsd/workflow/milestone-workflow.md` if present, else this skill) — pause after each task; wait for explicit `do next`
- **Commit Gate** — commit only after verified scope per `commit_cadence`
- **Remote Mutation Rule** — no push/PR without explicit user approval
- **Validation Rule** — run recorded validation commands before commit/push
- **Commit Message Format** — `feat(scope-slug): summary`; never use internal change folder names alone as the only message
- **Full Ticket-to-Plan Steps** (`skills/ticket-to-plan-openspec/SKILL.md`) — run every step in order
- **Prerequisite Skill Availability Gate** (`skills/ticket-to-plan-openspec/SKILL.md`) — grilling + brainstorming required
- **OpenSpec Planning Rule** (`skills/ticket-to-plan-openspec/SKILL.md`) — create artifacts only via OpenSpec CLI/`/opsx-*`
- **OpenSpec Artifact Completeness Rule** — all required change artifacts present
- **Full Plan Depth Rule** — proposal → specs → design → tasks before execution
- **Milestone Commit Cadence** — single commit per change after verification
- **Plan-Doc Embed Rule** — embed guardrails in `proposal.md`/`design.md` and summarize at top of `tasks.md`

### Embed into tasks.md

Copy the Guardrails list and commit-cadence note into the top of `tasks.md`.

## Stop conditions

Stop and ask if: Required Map incomplete, OpenSpec unavailable, grilling/brainstorming unavailable, required artifacts only partially created, or remote mutation would occur without approval.
