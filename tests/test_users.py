import os
from fastapi.testclient import TestClient
import backend.main as main

client = TestClient(main.app)


def admin_token():
    resp = client.post("/auth/token", data={"username": os.getenv("ADMIN_USERNAME", "admin"), "password": os.getenv("ADMIN_PASSWORD", "adminpass")})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_create_user_success():
    token = admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"username": "test_user1", "password": "Str0ng!Pass", "scopes": "admin"}
    r = client.post("/users/register", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "test_user1"


def test_create_user_conflict():
    token = admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"username": "test_user1", "password": "Str0ng!Pass", "scopes": "admin"}
    r = client.post("/users/register", json=payload, headers=headers)
    assert r.status_code == 409


def test_create_user_validation():
    token = admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    # weak password (no special char)
    payload = {"username": "baduser", "password": "Weakpass1", "scopes": "admin"}
    r = client.post("/users/register", json=payload, headers=headers)
    assert r.status_code == 422
