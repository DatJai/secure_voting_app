from .base_client import BaseClient


class VoterClient:
    def __init__(self, base_client: BaseClient):
        self.client = base_client

    def register(self, name: str, email: str):
        payload = {"name": name, "email": email}
        r = self.client.post("/voters/register", json=payload)
        r.raise_for_status()
        return r.json()

    def list(self):
        r = self.client.get("/voters/")
        r.raise_for_status()
        return r.json()
