from .base_client import BaseClient


class TokenClient:
    def __init__(self, base_client: BaseClient):
        self.client = base_client

    def public_key(self):
        r = self.client.get("/tokens/public_key")
        r.raise_for_status()
        return r.json()

    def issue_token(self, voter_id: str, blinded_message: str):
        payload = {"voter_id": voter_id, "blinded": blinded_message}
        r = self.client.post("/tokens/issue", json=payload)
        r.raise_for_status()
        return r.json()

    def tokens_by_voter(self, voter_id: str):
        r = self.client.get(f"/tokens/by_voter/{voter_id}")
        r.raise_for_status()
        return r.json()
