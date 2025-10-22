from db.connection import get_conn


class RevokedTokenRepository:
    def revoke_token(self, jti: str):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO revoked_tokens(jti, revoked_at) VALUES (%s, NOW()) ON CONFLICT (jti) DO NOTHING", (jti,))
        conn.commit()
        conn.close()

    def is_revoked(self, jti: str) -> bool:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM revoked_tokens WHERE jti=%s", (jti,))
            res = cur.fetchone()
        conn.close()
        return bool(res)
