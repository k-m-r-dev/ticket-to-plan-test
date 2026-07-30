# Benchmark prompt — protocol `abp-v1` arm `gsd` fixture `f2` r2

## Instructions

Follow skills/ticket-to-plan-gsd/SKILL.md with GSD MCP. Stop at plan-ready; do not implement.

## Skill

skills/ticket-to-plan-gsd/SKILL.md

## Fixture (Ambiguous ticket)

# Ticket: Local todo list API (incomplete)

We need a small **local HTTP API** for personal todos. Keep it simple.

## Goals

- Create, list, update, and delete todos
- Mark todos complete / incomplete
- Persist data so a restart does not lose todos
- Basic validation so bad input fails clearly

## Constraints

- Single-user / local use is fine
- No product design for multi-tenant or mobile apps yet
- Prefer something the team can run with one command

## Open questions (intentionally unresolved in this ticket)

- Language / framework?
- Database product?
- Exact URL paths and status codes?
- Error JSON shape?
- Filtering / pagination?
- Auth?

## Planning instruction

Clarify what you need, then produce a complete implementation plan. Do not implement code in the planning run.


## Output

Write plan artifacts into `benchmark/runs/abp-v1/f2/gsd/r2/artifacts/`.
Fill meta.json started_at/ended_at, tool_calls, tokens when done.
