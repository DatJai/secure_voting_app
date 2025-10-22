# Postgres connection manager
# db/connection.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env.backend file
env_path = Path(__file__).parent.parent / ".env.backend"
load_dotenv(dotenv_path=env_path)

# Fallback: also try loading from .env if .env.backend not found
if not os.getenv("DATABASE_URL"):
    load_dotenv()


# Singleton connection getter for repository modules
def get_conn():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError(
            "DATABASE_URL environment variable not set. "
            "Please ensure .env.backend or .env file exists with DATABASE_URL configured."
        )
    return psycopg2.connect(db_url, cursor_factory=RealDictCursor)
