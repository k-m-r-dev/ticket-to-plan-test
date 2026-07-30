"""Black-box oracle tests for fixtures/todo-api/SPEC.md."""

from __future__ import annotations

import os
import uuid

import httpx
import pytest

BASE = os.environ.get("ORACLE_BASE_URL", "http://127.0.0.1:8080").rstrip("/")


@pytest.fixture(scope="module")
def client():
    with httpx.Client(base_url=BASE, timeout=10.0) as c:
        yield c


def test_health(client: httpx.Client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_create_and_get(client: httpx.Client):
    r = client.post("/todos", json={"title": "oracle-item"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "oracle-item"
    assert body["completed"] is False
    assert "id" in body and "created_at" in body and "updated_at" in body
    tid = body["id"]
    g = client.get(f"/todos/{tid}")
    assert g.status_code == 200
    assert g.json()["id"] == tid


def test_empty_title_validation(client: httpx.Client):
    r = client.post("/todos", json={"title": "   "})
    assert r.status_code == 400
    err = r.json()["error"]
    assert err["code"] == "validation_error"
    assert "message" in err


def test_list_and_filter(client: httpx.Client):
    a = client.post("/todos", json={"title": f"open-{uuid.uuid4()}", "completed": False}).json()
    b = client.post("/todos", json={"title": f"done-{uuid.uuid4()}", "completed": True}).json()
    listed = client.get("/todos")
    assert listed.status_code == 200
    assert isinstance(listed.json(), list)
    done = client.get("/todos", params={"completed": "true"})
    assert done.status_code == 200
    ids = {t["id"] for t in done.json()}
    assert b["id"] in ids
    assert a["id"] not in ids
    bad = client.get("/todos", params={"completed": "maybe"})
    assert bad.status_code == 400


def test_patch_delete_404(client: httpx.Client):
    missing = str(uuid.uuid4())
    assert client.get(f"/todos/{missing}").status_code == 404
    assert client.patch(f"/todos/{missing}", json={"title": "x"}).status_code == 404
    assert client.delete(f"/todos/{missing}").status_code == 404
    created = client.post("/todos", json={"title": "to-patch"}).json()
    tid = created["id"]
    empty = client.patch(f"/todos/{tid}", json={})
    assert empty.status_code == 400
    patched = client.patch(f"/todos/{tid}", json={"completed": True, "title": "patched"})
    assert patched.status_code == 200
    assert patched.json()["completed"] is True
    assert patched.json()["title"] == "patched"
    deleted = client.delete(f"/todos/{tid}")
    assert deleted.status_code == 204
    assert client.get(f"/todos/{tid}").status_code == 404
