# db/repositories/ballot_repository.py
from db.connection import get_conn

class BallotRepository:
    def add_ballot(self, ballot_id: str, candidate: str, token_hash: str, encrypted: bool = True):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ballots(ballot_id, candidate, token_hash, encrypted)
                VALUES (%s, %s, %s, %s)
            """, (ballot_id, candidate, token_hash, encrypted))
        conn.commit()
        conn.close()

    def get_all_ballots(self):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ballots ORDER BY ballot_id")
            ballots = cur.fetchall()
        conn.close()
        return ballots
