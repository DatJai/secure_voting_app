# db/repositories/mixnet_repository.py
from db.connection import get_conn

class MixNetRepository:
    def save_proof(self, proof: dict):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO mixnet_proofs(layer, input_count, output_count, proof_hash)
                VALUES (%s, %s, %s, %s)
            """, (proof["layer"], proof["inputCount"], proof["outputCount"], proof["proof"]))
        conn.commit()
        conn.close()
