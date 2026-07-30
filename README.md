# ticket-to-plan vs OpenSpec benchmark

GSD sandbox that compares **four ways** to turn a ticket/SPEC into an implementation plan — same product problem, locked scoring rules.

| Method | What it uses |
| --- | --- |
| **GSD** | `ticket-to-plan` + GSD workflow tools |
| **OpenSpec** | Same skill steps, OpenSpec CLI / artifacts |
| **Skill only** | `ticket-to-plan` with plain markdown (no GSD/OpenSpec) |
| **Native** | Plain AI planning — no skill |

**Subject:** greenfield Rust Todo HTTP API (Axum + SQLite).

## Current status (abp-v1)

Acceptance Benchmark Protocol matrix is **complete for plan quality**:

- 24 planning runs (4 methods × 2 inputs × 3 repeats)
- Automated checklist scores + blind human review
- Results: [`docs/benchmark/ACCEPTANCE_REPORT.md`](docs/benchmark/ACCEPTANCE_REPORT.md)
- Team deck: [`docs/benchmark/ticket-to-plan-abp-team-update.pptx`](docs/benchmark/ticket-to-plan-abp-team-update.pptx)

**Headline:** on this fixture, all methods hit ~100% checklist quality; **cost** (time / tokens / tools) is where they differ. OpenSpec matched GSD on plan quality. Full protocol acceptance still open on “build from plan” executes (optional).

## Quick links

| Doc | Purpose |
| --- | --- |
| [`docs/benchmark/PROTOCOL.md`](docs/benchmark/PROTOCOL.md) | Frozen rules (do not edit post-hoc) |
| [`docs/benchmark/OPERATOR_RUNBOOK.md`](docs/benchmark/OPERATOR_RUNBOOK.md) | How to run planning slots |
| [`docs/benchmark/ACCEPTANCE_REPORT.md`](docs/benchmark/ACCEPTANCE_REPORT.md) | R1–R4 outcomes + claims |
| [`docs/benchmark/ticket-to-plan-openspec-benchmark-explained.md`](docs/benchmark/ticket-to-plan-openspec-benchmark-explained.md) | Plain-language walkthrough |
| [`benchmark/runs/abp-v1/COMPARISON.md`](benchmark/runs/abp-v1/COMPARISON.md) | Score / cost table |
| [`benchmark/README.md`](benchmark/README.md) | Harness commands |

## Layout

```text
fixtures/todo-api/              Locked SPEC + gold checklist + oracle tests
fixtures/todo-api-ambiguous/    Vague ticket + sealed answer key
skills/                         ticket-to-plan variants (gsd / openspec / no-tools)
benchmark/                      Python harness + abp-v1 run artifacts
apps/todo-api/                  Rust skeleton (for optional execute-to-score)
apps/todo-api-reference/        Python reference server (oracle proof)
docs/benchmark/                 Protocol, runbooks, reports, deck
openspec/                       OpenSpec project config + change artifacts from runs
```

## Setup

```bash
# Node (OpenSpec CLI via npx)
npm install

# Python harness + Excel scorecard deps
python3 -m venv .venv
source .venv/bin/activate
pip install openpyxl tiktoken
# optional DeepEval package:
# pip install -r benchmark/acceptance/requirements.txt
```

OpenSpec: `npx openspec …` (project-local; see `package.json`).

## Reproduce reports

```bash
source .venv/bin/activate
python3 benchmark/report_abp.py --protocol abp-v1
python3 benchmark/disagreement_s1_s2.py --protocol abp-v1
```

Planning matrix / S2 draft drivers: see [`docs/benchmark/AGENT_RUNNER.md`](docs/benchmark/AGENT_RUNNER.md) and [`docs/benchmark/S2_DRAFT_AGENT.md`](docs/benchmark/S2_DRAFT_AGENT.md). Run those from **your own terminal**, not from a Cursor chat.

## Remote

Canonical GitHub repo: [k-m-r-dev/ticket-to-plan-test](https://github.com/k-m-r-dev/ticket-to-plan-test)
