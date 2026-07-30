# F1 execute oracle — Todo HTTP API

Black-box contract tests derived **only** from [`../SPEC.md`](../SPEC.md).  
Locked before ABP plan selection for execute-to-score.

## How to run

Against a server listening on `ORACLE_BASE_URL` (default `http://127.0.0.1:8080`):

```bash
pip install -r fixtures/todo-api/oracle/requirements.txt
ORACLE_BASE_URL=http://127.0.0.1:8080 pytest fixtures/todo-api/oracle -v
```

## Cases covered

- GET /health → 200 `{"status":"ok"}`
- POST /todos validation + 201 shape
- GET /todos list + completed filter
- GET/PATCH/DELETE by id + 404
- Error envelope `error.code` / `error.message`
