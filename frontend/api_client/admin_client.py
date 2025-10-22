from .base_client import BaseClient


class AdminClient:
    def __init__(self, base_client: BaseClient):
        self.client = base_client

    def login(self, username: str, password: str):
        # OAuth2 password grant via form data
        r = self.client.session.post(f"{self.client.base}/auth/token", data={"username": username, "password": password})
        r.raise_for_status()
        data = r.json()
        self.client.set_tokens(data.get("access_token"), data.get("refresh_token"))
        return data

    def create_user(self, username: str, password: str, scopes: str = "admin"):
        payload = {"username": username, "password": password, "scopes": scopes}
        r = self.client.post("/users/register", json=payload)
        return r.json()

    def list_users(self):
        r = self.client.get("/users/")
        return r.json()

    def revoke_current(self):
        r = self.client.post("/auth/revoke")
        return r.json()

    def run_mixnet(self, layers: int = 3):
        r = self.client.post("/mixnet/run", json={"layers": layers})
        return r.json()
# frontend/api_client/admin_client.py
from .base_client import BaseClient
from fastapi import HTTPException  # or use requests exceptions

class AdminClient:
    def __init__(self, base_client: BaseClient):
        self.client = base_client

    def login(self, username: str, password: str):
        # oauth2 form login
        resp = self.client.session.post(f"{self.client.base}/auth/token", data={"username": username, "password": password})
        resp.raise_for_status()
        data = resp.json()
        self.client.set_tokens(data["access_token"], data.get("refresh_token"))
        return data

    def create_user(self, username: str, password: str, scopes: str = "admin"):
        payload = {"username": username, "password": password, "scopes": scopes}
        resp = self.client.post("/users/register", json=payload)
        return resp.json()

    def list_users(self):
        resp = self.client.get("/users/")
        return resp.json()