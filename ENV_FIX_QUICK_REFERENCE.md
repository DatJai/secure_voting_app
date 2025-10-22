# Quick Reference: .env Loading Fix

## What Was Fixed?

**Problem:** Backend couldn't load `.env.backend` because `load_dotenv()` was looking for `.env` by default.

**Solution:** Explicitly specify `.env.backend` path in `load_dotenv()` call.

---

## Files Changed

### 1. `/workspace/backend/db/connection.py`

```python
# OLD
load_dotenv()

# NEW
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env.backend"
load_dotenv(dotenv_path=env_path)
if not os.getenv("DATABASE_URL"):
    load_dotenv()
```

### 2. `/workspace/backend/main.py`

```python
# OLD
from fastapi import FastAPI

# NEW
from fastapi import FastAPI
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env.backend"
load_dotenv(dotenv_path=env_path)
if not os.getenv("DATABASE_URL"):
    load_dotenv()
```

---

## Quick Test

```bash
# Test 1: Check environment loads
cd /workspace/backend
python -c "import os; from dotenv import load_dotenv; from pathlib import Path; env_path = Path('.') / '.env.backend'; load_dotenv(dotenv_path=env_path); print(os.getenv('DATABASE_URL'))"

# Should output: postgresql://postgres:password@localhost:5432/voting_db

# Test 2: Test connection
python -c "from db.connection import get_conn; conn = get_conn(); print('✅ Connection OK'); conn.close()"

# Test 3: Start backend
python main.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DATABASE_URL not set` | Ensure `.env.backend` exists with `DATABASE_URL` line |
| Still getting None | Check file path: `/workspace/backend/.env.backend` |
| Connection refused | PostgreSQL not running: `sudo systemctl start postgresql` |

---

## Summary

✅ **Before:** `load_dotenv()` → looks for `.env` → fails  
✅ **After:** `load_dotenv(dotenv_path=".env.backend")` → finds file → works
