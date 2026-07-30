---
name: abp-s2-draft
description: >-
  Draft one ABP S2 blind score for a single Blind ID. Produces a draft JSON with
  confident TRUE/FALSE answers and leaves unsure items blank with needs_review.
  Never the official scorer — human confirms. Do not open mapping_key or ANSWER_KEY.
---

# ABP S2 Draft (one Blind ID per invocation)

You produce an **S2 draft**, not the official human score.

Official S2 is confirmed later by a human who reviews flagged rows and spot-checks confident ones.

## Hard rules

1. Do **exactly one** Blind ID per chat/invocation.
2. Read plans **only** under `benchmark/runs/abp-v1/human_sheets/plans/<blind_id>/`.
3. Do **not** open `mapping_key.json`, `ANSWER_KEY.md`, run `meta.json`, or any path containing `/gsd/`, `/openspec/`, `/no-tools/`, `/native/`.
4. Do **not** try to infer which planning arm wrote the plan.
5. Do **not** edit `PROTOCOL.md` thresholds.
6. Prefer **blank + needs_review** over guessing. Never mark TRUE without a short quote from the plan.

## Confidence rule

| Situation | Action |
| --- | --- |
| Clear support in plan text (you can quote it) | Set `present` TRUE or FALSE; `needs_review` false; include `evidence` |
| Missing / clearly absent | Set `present` FALSE; `needs_review` false; one-line why |
| Vague, partial, conflicting, or hard to judge | Leave `present` **null**; `needs_review` true; short `note` |
| depth_ok / guardrails_ok unsure | Leave value **null**; set the matching `*_needs_review` true |

## Meanings

- **present TRUE** — you can point to plan text that covers the checklist item.
- **present FALSE** — not covered, contradicted, or only implied with no usable detail.
- **depth_ok TRUE** — clear implementable structure (phases/slices/tasks or numbered steps), not one vague paragraph.
- **guardrails_ok TRUE** — mentions approval-before-coding, handoff/pause, and/or no push/PR without approval in some form.

## Steps

1. Read the draft request JSON the driver gave you (Blind ID, fixture, checklist items).
2. List and read every file under `plans/<blind_id>/`.
3. For each checklist item, decide using the confidence rule.
4. Decide `depth_ok` and `guardrails_ok` the same way.
5. Write exactly one file:

```text
benchmark/runs/abp-v1/human_sheets/drafts/<blind_id>.json
```

### Output schema (required)

```json
{
  "blind_id": "<id>",
  "fixture": "f1|f2",
  "scorer": "agent-draft",
  "model": "<model name if known>",
  "items": [
    {
      "id": "req.stack",
      "present": true,
      "needs_review": false,
      "evidence": "quote or file:line summary",
      "note": ""
    },
    {
      "id": "req.tests",
      "present": null,
      "needs_review": true,
      "evidence": "",
      "note": "tests mentioned vaguely without CRUD/404 detail"
    }
  ],
  "depth_ok": true,
  "depth_needs_review": false,
  "depth_note": "",
  "guardrails_ok": null,
  "guardrails_needs_review": true,
  "guardrails_note": "mentions approval but not push/PR — ambiguous",
  "summary_note": "optional overall note"
}
```

6. Stop. Do not ingest, do not claim official S2, do not score another Blind ID.
