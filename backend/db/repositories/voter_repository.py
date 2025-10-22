# db/repositories/voter_repository.py
from db.connection import get_conn

class VoterRepository:
    def add_voter(self, voter_id: str, name: str, email: str = None):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO voters(voter_id, name, email, has_token, has_voted)
                VALUES (%s, %s, %s, false, false)
                ON CONFLICT (voter_id) DO NOTHING
            """, (voter_id, name, email))
        conn.commit()
        conn.close()

    def get_all_voters(self):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM voters ORDER BY voter_id")
            result = cur.fetchall()
        conn.close()
        return result

    def get_last_voter(self):
        """Get the last registered voter (by voter_id)"""
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM voters ORDER BY voter_id DESC LIMIT 1")
            result = cur.fetchone()
        conn.close()
        return result

    def update_token_status(self, voter_id: str, has_token: bool):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("UPDATE voters SET has_token=%s WHERE voter_id=%s", (has_token, voter_id))
        conn.commit()
        conn.close()

    def mark_voted(self, voter_id: str):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("UPDATE voters SET has_voted=true WHERE voter_id=%s", (voter_id,))
        conn.commit()
        conn.close()
