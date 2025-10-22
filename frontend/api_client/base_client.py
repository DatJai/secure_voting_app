import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")


class BaseClient:
    def __init__(self):
        self.base = BASE
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None

    def set_tokens(self, access_token: str | None, refresh_token: str | None = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        if access_token:
            self.session.headers.update({"Authorization": f"Bearer {access_token}"})
        else:
            self.session.headers.pop("Authorization", None)

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.base}{path}"
        resp = self.session.request(method, url, **kwargs)
        # try refresh once on 401
        if resp.status_code == 401 and self.refresh_token:
            if self._try_refresh():
                resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def _try_refresh(self) -> bool:
        try:
            r = self.session.post(f"{self.base}/auth/refresh", json={"refresh_token": self.refresh_token})
            if r.status_code == 200:
                data = r.json()
                self.set_tokens(data.get("access_token"), data.get("refresh_token", self.refresh_token))
                return True
        except Exception:
            pass
        return False
# frontend/api_client/base_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BACKEND_URL", "http://localhost:8000")

class BaseClient:
    def __init__(self):
        self.base = BASE.rstrip("/")
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()

    def set_tokens(self, access_token: str, refresh_token: str | None = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        if access_token:
            self.session.headers.update({"Authorization": f"Bearer {access_token}"})
        else:
            self.session.headers.pop("Authorization", None)

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.base}{path}"
        resp = self.session.request(method, url, **kwargs)
        # If 401 and we have a refresh token, try refresh once
        if resp.status_code == 401 and self.refresh_token:
            if self._try_refresh():
                resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def _try_refresh(self) -> bool:
        try:
            r = self.session.post(f"{self.base}/auth/refresh", json={"refresh_token": self.refresh_token})
            if r.status_code == 200:
                tokens = r.json()
                self.set_tokens(tokens["access_token"], getattr(tokens, "refresh_token", self.refresh_token))
                return True
        except Exception:
            pass
        return False