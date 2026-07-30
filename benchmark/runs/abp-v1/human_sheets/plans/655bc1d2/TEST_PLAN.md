# Test plan — Todo HTTP API (native arm, ABP f1)

Integration tests use in-process HTTP (Axum `TestClient` / tower service tests) against an isolated SQLite database per test or per suite. Prefer `tests/integration.rs` with a shared `setup_app()` helper.

## Harness

| Concern | Approach |
| --- | --- |
| App under test | `create_app(pool)` from `lib.rs` |
| DB isolation | Temp file via `tempfile` or unique `DATABASE_URL` per test |
| Client | `axum_test::TestClient` or `tower::ServiceExt` + `Request` |
| Assertions | Status code, JSON body, empty body for `204` |

## Required integration tests

### CRUD happy path

1. **create** — `POST /todos` with `{ "title": "buy milk" }` → `201`, body has UUID `id`, `completed: false`, RFC 3339 timestamps.
2. **list** — `GET /todos` → `200`, array includes created todo.
3. **get** — `GET /todos/:id` → `200`, same todo.
4. **patch** — `PATCH /todos/:id` with `{ "completed": true }` → `200`, `completed` true, `updated_at` changed.
5. **delete** — `DELETE /todos/:id` → `204`; subsequent `GET` → `404`.

### List filter (`completed` query)

6. **filter true** — Create todos with `completed` true/false; `GET /todos?completed=true` returns only completed.
7. **filter false** — `GET /todos?completed=false` returns only incomplete.
8. **invalid filter** — `GET /todos?completed=maybe` → `400` `validation_error`.

### Validation

9. **empty title** — `POST /todos` `{ "title": "" }` or whitespace-only → `400` `validation_error`.
10. **overlong title** — `POST /todos` with title length 201 → `400` `validation_error`.
11. **empty PATCH body** — `PATCH /todos/:id` with `{}` → `400` `validation_error`.
12. **PATCH title validation** — `PATCH` with overlong or empty title → `400` `validation_error`.

### 404 paths

13. **get 404** — `GET /todos/{random-uuid}` → `404` `not_found`.
14. **patch 404** — `PATCH /todos/{random-uuid}` → `404` `not_found`.
15. **delete 404** — `DELETE /todos/{random-uuid}` → `404` `not_found`.

### Health

16. **health** — `GET /health` → `200` `{ "status": "ok" }`.

### Error envelope

17. **error shape** — On at least one `400` and one `404`, assert JSON matches `{ "error": { "code", "message" } }` and codes include `validation_error` and `not_found` as appropriate.

## Optional (not required by SPEC)

- Repository unit tests for title trim and timestamp updates.
- Startup test that migrations apply idempotently on second pool init.

## Test execution gate

All integration tests must pass before milestone completion:

```bash
cargo test
cargo clippy -- -D warnings
```
