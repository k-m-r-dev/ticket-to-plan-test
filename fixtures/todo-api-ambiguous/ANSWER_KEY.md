# Answer key — F2 ambiguous todo API

Use **only for scoring / after grilling**. Operators must not paste this into planning prompts.

When the arm resolves ambiguity (grilling or invention), score whether the plan lands on these gold decisions (aligned with F1 SPEC for comparability):

| Decision id | Gold resolution |
| --- | --- |
| `dec.stack` | Rust + Axum + Tokio + SQLite via sqlx |
| `dec.model` | Todo: id (UUID), title, completed, created_at, updated_at |
| `dec.routes` | POST/GET/PATCH/DELETE `/todos`, GET `/todos/:id`, GET `/health` |
| `dec.filter` | List supports `?completed=true\|false` |
| `dec.validation` | Title trimmed length 1..=200; empty PATCH rejected |
| `dec.errors` | `{ "error": { "code", "message" } }` with validation_error / not_found / internal_error |
| `dec.config` | DATABASE_URL, HOST, PORT with documented defaults |
| `dec.tests` | Integration tests for CRUD, validation, 404 |
| `dec.oos` | Auth, UI, pagination, k8s **not** required |

## Scoring note

S2 for F2 uses `decision_checklist.json` (correct / incorrect / missing), not F1 keyword coverage alone.
