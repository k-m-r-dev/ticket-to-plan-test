# Benchmark prompt — protocol `abp-v1` arm `native` fixture `f2` r2

## Instructions

No ticket-to-plan skill. Produce a complete implementation plan. Write into artifacts/. Do not implement.

## Skill

(none — native)

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

Write plan artifacts into `benchmark/runs/abp-v1/f2/native/r2/artifacts/`.
Fill meta.json started_at/ended_at, tool_calls, tokens when done.
