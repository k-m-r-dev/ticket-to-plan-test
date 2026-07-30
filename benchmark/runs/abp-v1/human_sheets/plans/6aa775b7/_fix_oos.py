from pathlib import Path

paths = [
    Path("/Users/khandkermahmudur/Workspace/openspec-test/.gsd/phases/01-todo-http-api/01-ROADMAP.md"),
    Path("/Users/khandkermahmudur/Workspace/openspec-test/benchmark/runs/abp-v1/f1/gsd/r1/artifacts/01-ROADMAP.md"),
]
old = """## Boundary Map

**In:** Rust Axum HTTP API, SQLite via sqlx, migrations, JSON CRUD + completed filter, health, integration tests.

**Out:** Auth, multi-user, pagination/sorting, soft deletes, UI/CLI client, OpenAPI, Docker/K8s, rate limiting/CORS policy, GraphQL/gRPC."""
new = """## Boundary Map

**In:** Rust Axum HTTP API, SQLite via sqlx, migrations, JSON CRUD + completed filter, health, integration tests.

## Out of scope

Auth, multi-user, pagination/sorting, soft deletes, UI/CLI client, OpenAPI, Docker/K8s, rate limiting/CORS policy, GraphQL/gRPC."""
for p in paths:
    t = p.read_text()
    if old not in t:
        print(p, "pattern missing")
        continue
    p.write_text(t.replace(old, new))
    print(p, "updated")
