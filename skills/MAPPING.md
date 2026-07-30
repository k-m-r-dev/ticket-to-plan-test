# GSD ↔ OpenSpec Mapping (ticket-to-plan thin adapter)

| GSD concept | OpenSpec concept |
| --- | --- |
| Top-level unit (milestone / phase), e.g. `M001` | Change folder `openspec/changes/<kebab-name>/` |
| Slice `S01` | Heading / task group inside `tasks.md` |
| Task `T01` | Checkbox item in `tasks.md` |
| `.gsd` DB + projected markdown | Files under `openspec/changes/<name>/` |
| `gsd_plan_milestone` / `gsd_plan_slice` / `gsd_plan_task` | `npx openspec new change`, `openspec instructions`, `/opsx-propose` |
| `gsd_progress` / `gsd_task_complete` | `/opsx-apply` + editing task checkboxes |
| `CONTEXT.md` / `ROADMAP.md` Delivery section | `## Delivery & Guardrails` in `proposal.md` or `design.md` |
| `.gsd/DELIVERY-PROFILE.md` | Still read for delivery defaults (not replaced by OpenSpec) |
| `.gsd/workflow/*.md` guardrail sources | Cite when present; else cite `skills/ticket-to-plan-openspec/SKILL.md` |
| Compat / reproject scripts | Not applicable — use `npx openspec status --change <name>` |

## Artifact completeness (spec-driven schema)

Required before apply: `proposal.md`, `specs/**/spec.md`, `design.md`, `tasks.md`.

## CLI entrypoints (this repo)

OpenSpec is a **local** npm dependency (not global):

```bash
npx openspec --version
npx openspec init --tools cursor   # already done
npx openspec new change "<name>"
npx openspec status --change "<name>" --json
```
