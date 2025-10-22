from .base_client import BaseClient


class BallotClient:
    def __init__(self, base_client: BaseClient):
        self.client = base_client

    def cast(self, voter_id: str, token: str, vote: dict):
        payload = {"voter_id": voter_id, "token": token, "vote": vote}
        r = self.client.post("/ballots/cast", json=payload)
        r.raise_for_status()
        return r.json()

    def list(self):
        r = self.client.get("/ballots/")
        r.raise_for_status()
        return r.json()
