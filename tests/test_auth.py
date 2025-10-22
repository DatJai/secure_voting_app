import os
import time
from fastapi.testclient import TestClient

import backend.main as main

client = TestClient(main.app)


def get_token(username="admin", password="adminpass"):
    resp = client.post("/auth/token", data={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["access_token"], resp.json().get("refresh_token")


def test_token_and_protected_access():
    access, refresh = get_token()
    headers = {"Authorization": f"Bearer {access}"}
    # mixnet/run requires admin
    r = client.post("/mixnet/run", headers=headers)
    # mixnet may return no ballots but should authorize
    assert r.status_code in (200, 400)


def test_revocation():
    access, _ = get_token()
    headers = {"Authorization": f"Bearer {access}"}
    # revoke token
    r = client.post("/auth/revoke", headers=headers)
    assert r.status_code == 200
    # now protected call should fail
    r2 = client.post("/mixnet/run", headers=headers)
    assert r2.status_code == 401


def test_refresh_flow():
    access, refresh = get_token()
    assert refresh is not None
    r = client.post("/auth/refresh", json={"refresh_token": refresh})
    assert r.status_code == 200
    new_access = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {new_access}"}
    r2 = client.post("/mixnet/run", headers=headers)
    assert r2.status_code in (200, 400)
