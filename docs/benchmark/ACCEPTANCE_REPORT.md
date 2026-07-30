# Acceptance Report — abp-v1

**Generated:** 2026-07-30  
**Protocol:** [`PROTOCOL.md`](PROTOCOL.md) (frozen)  
**Evidence:** [`COMPARISON.md`](../../benchmark/runs/abp-v1/COMPARISON.md), [`DISAGREEMENT_S1_S2.md`](../../benchmark/runs/abp-v1/DISAGREEMENT_S1_S2.md), [`s2_summary.json`](../../benchmark/runs/abp-v1/human_sheets/s2_summary.json)  
**Stance:** Tool-agnostic. Rules evaluated on complete plan-quality data; execute still open.

## Executive status

| Gate | Status |
| --- | --- |
| Protocol frozen + fixture/skill hashes | **PASS** |
| 24 independent planning runs (`plan_ready`) | **PASS** |
| S1 automated scores | **PASS** (24/24; S1↔S2 deltas all 0.00) |
| S2 blind human ingest (primary) | **PASS** (24/24 complete sheets) |
| S3 DeepEval | **SKIPPED** (operator choice; supporting only) |
| Execute-to-score (4 F1 arm medians) | **NOT RUN** (reference oracle proof only) |
| Pre-registered rules R1–R4 | **FAIL overall** (see below — valid scientific outcome) |

**Overall acceptance:** **NOT PASSED** under the frozen rules.  
Plan-quality matrix is complete and decision-useful for **cost / process** claims. Full ABP acceptance still requires R4 executes (and R2/R3 as written require ticket-to-plan arms to *beat* native, not tie).

## Headline (plain language)

On this Todo API fixture set, **all four planning methods scored the same on S2 quality** (coverage 1.00, depth yes, guardrails yes — every arm × every fixture × every replicate).

They did **not** score the same on cost:

| fixture | arm | mean wall (s) | mean tiktoken | mean tool calls |
| --- | --- | ---: | ---: | ---: |
| f1 | gsd | 247 | 5178 | 15 |
| f1 | openspec | 159* | 7304* | 30* |
| f1 | no-tools | 89 | 4505 | 27 |
| f1 | native | 36 | 4433 | 27 |
| f2 | gsd | 186 | 4306 | 52 |
| f2 | openspec | 83 | 6167 | 35 |
| f2 | no-tools | 39 | 3591 | 32 |
| f2 | native | 60 | 3486 | 27 |

\*COMPARISON.md currently lists f1/openspec **n=4** (matrix slots are n=3; one superseded score may be leaking into the aggregator — treat openspec cost as directional until cleaned). Official planning slots: **24**.

**S1 vs S2:** no coverage disagreements (all deltas +0.00).

## Pre-registered rules

### R1 — F1 method parity (gsd vs openspec) → **PASS**

| metric | gsd mean | openspec mean | \|Δ\| | threshold |
| --- | ---: | ---: | ---: | ---: |
| S2 coverage | 1.00 | 1.00 | 0.00 | ≤ 0.05 |
| S2 depth | 1.00 | 1.00 | 0.00 | ≤ 0.05 |

GSD and OpenSpec are within the frozen parity band on F1 plan quality.

### R2 — F1 guardrails vs native → **FAIL**

Rule requires each of `gsd`, `openspec`, `no-tools` to **exceed** native mean S2 guardrail fidelity.

| arm | mean S2 guardrails (F1) |
| --- | ---: |
| gsd | 1.00 |
| openspec | 1.00 |
| no-tools | 1.00 |
| native | 1.00 |

All arms tied at ceiling. Ticket-to-plan arms did **not** exceed native → **FAIL with data**.

Interpretation: on a fully locked SPEC, native plans also cited enough process language to pass the human guardrail check. This fixture did not discriminate guardrail quality.

### R3 — F2 ambiguity → **FAIL**

Rule requires each ticket-to-plan arm’s mean S2 answer-key decision correctness to **exceed** native.

| arm | mean S2 coverage (F2) |
| --- | ---: |
| gsd | 1.00 |
| openspec | 1.00 |
| no-tools | 1.00 |
| native | 1.00 |

Again a ceiling tie → **FAIL with data**.

Interpretation: the ambiguous ticket still left enough recoverable intent that every method hit the decision checklist. Stronger discrimination would need a harder F2 (or item-level partial credit), under a **new protocol version**.

### R4 — Execute disclosure → **FAIL** (not run)

| arm | oracle pass rate | status |
| --- | --- | --- |
| gsd | — | PENDING_PLAN_SELECTION |
| openspec | — | PENDING_PLAN_SELECTION |
| no-tools | — | PENDING_PLAN_SELECTION |
| native | — | PENDING_PLAN_SELECTION |
| reference (infra proof) | 5/5 | PASS (not an arm) |

Protocol: failing to run or hiding a rate **fails acceptance**. Rates are disclosed here as **not run**.

## Claims we can make (plan-only ABP)

1. **OpenSpec adapter is quality-parity with GSD on this matrix** (R1 PASS).  
2. **No plan-quality winner among the four arms** on F1/F2 S2 coverage/depth/guardrails — all saturated.  
3. **Cost differs:** native / no-tools are faster and use fewer tokens; GSD is slowest on wall; OpenSpec tends to higher token counts.  
4. **S1 keyword scoring matched S2** on coverage for every run in this matrix (supporting, not primary).

## Claims we must not make yet

1. Full **abp-v1 acceptance PASS** (R2, R3, R4 failed / unmet).  
2. “Ticket-to-plan beats native on guardrails or ambiguity” (R2/R3 failed — tie at ceiling).  
3. “Plans implement cleanly” (R4 executes not done).  
4. DeepEval faithfulness rankings (S3 skipped).

## Recommended next steps (outside this report)

1. Optional: clean COMPARISON aggregator so f1/openspec n=3 (exclude superseded).  
2. Optional: run R4 median F1 executes → fill pass rates → re-evaluate acceptance.  
3. If discrimination is required: design **abp-v2** with harder F2 / partial-credit guardrails (protocol bump + full re-run).  
4. Team narrative: quality parity + cost tradeoff; OpenSpec is a viable GSD substitute for ticket-to-plan on this subject.

## Limitations

- S2 used agent draft + human review queue (operator remained authority).  
- Ceiling effects limit rule sensitivity when every arm scores 1.00.  
- Cursor billing tokens remain partially opaque; TikToken is an estimate.  
- Human sheets must stay operator-owned; do not treat agent drafts as official S2.
