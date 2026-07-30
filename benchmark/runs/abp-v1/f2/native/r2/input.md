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
