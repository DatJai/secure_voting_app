from db.connection import get_conn
from typing import Optional
import psycopg2


# Fallback in-memory users for environments without a DB (tests/dev)
_IN_MEMORY_USERS: dict[str, dict] = {}


class UserRepository:
    def create_user(self, username: str, hashed_password: str, scopes: str = "admin"):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users(username, password_hash, scopes)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO NOTHING
                """, (username, hashed_password, scopes))
            conn.commit()
            conn.close()
        except (Exception, psycopg2.OperationalError):
            # fallback to in-memory store
            if username not in _IN_MEMORY_USERS:
                _IN_MEMORY_USERS[username] = {"username": username, "password_hash": hashed_password, "scopes": scopes}

    def get_user(self, username: str) -> Optional[dict]:
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username=%s", (username,))
                user = cur.fetchone()
            conn.close()
            return user
        except (Exception, psycopg2.OperationalError):
            return _IN_MEMORY_USERS.get(username)
