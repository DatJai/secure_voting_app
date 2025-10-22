# db/repositories/log_repository.py
from db.connection import get_conn
from datetime import datetime

class LogRepository:
    def add_log(self, message: str, log_type: str = "info"):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO logs(message, log_type, created_at)
                VALUES (%s, %s, %s)
            """, (message, log_type, datetime.now()))
        conn.commit()
        conn.close()

    def get_all_logs(self):
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM logs ORDER BY created_at DESC")
            logs = cur.fetchall()
        conn.close()
        return logs
