# Test plan — Local Todo HTTP API (native arm, f2 r2)

Integration tests run in-process against Axum via `TestClient` or tower `ServiceExt`. Each test uses an isolated SQLite database (temp file or unique `DATABASE_URL`).

## Test harness

| Concern | Approach |
| --- | --- |
| App factory | `create_app(pool)` from `lib.rs` |
| DB isolation | `tempfile` or per-test `sqlite:` path |
| HTTP client | `axum_test::TestClient` or manual `Request` via `ServiceExt` |
| Assertions | Status code, JSON body, empty body for `204` |

## Required integration tests

### CRUD happy path

1. **create** — `POST /todos` `{ "title": "walk dog" }` → `201`; body has UUID `id`, `completed: false`, RFC 3339 `created_at` / `updated_at`.
2. **list** — `GET /todos` → `200`; array contains created todo.
3. **get** — `GET /todos/:id` → `200`; same fields.
4. **patch complete** — `PATCH /todos/:id` `{ "completed": true }` → `200`; `completed` true; `updated_at` ≥ prior value.
5. **delete** — `DELETE /todos/:id` → `204`; `GET /todos/:id` → `404` `not_found`.

### Completed filter

6. **filter true** — Seed completed and incomplete todos; `GET /todos?completed=true` returns only completed items.
7. **filter false** — `GET /todos?completed=false` returns only incomplete items.
8. **invalid filter** — `GET /todos?completed=maybe` → `400` `validation_error`.

### Validation

9. **empty title on create** — `POST /todos` `{ "title": "" }` or whitespace-only → `400` `validation_error`.
10. **overlong title on create** — title length 201 → `400` `validation_error`.
11. **empty PATCH body** — `PATCH /todos/:id` `{}` → `400` `validation_error`.
12. **PATCH title validation** — empty or overlong title on PATCH → `400` `validation_error`.

### 404 paths

13. **get missing** — `GET /todos/{random-uuid}` → `404` `not_found`.
14. **patch missing** — `PATCH /todos/{random-uuid}` → `404` `not_found`.
15. **delete missing** — `DELETE /todos/{random-uuid}` → `404` `not_found`.

### Health

16. **health** — `GET /health` → `200` `{ "status": "ok" }`.

### Error envelope

17. **shape** — On at least one `400` and one `404`, assert body matches `{ "error": { "code", "message" } }` with appropriate codes (`validation_error`, `not_found`).

### Persistence (optional smoke)

18. **restart survival** — Create todo, tear down pool, re-init against same `DATABASE_URL`, `GET /todos` still returns todo.

## Optional unit tests

- Repository: title trim, timestamp update on PATCH.
- Config: default env values.
- Migration idempotency on second `migrate!` call.

## Test execution gate

Before considering the milestone done:

```bash
cargo test
cargo clippy -- -D warnings
```
