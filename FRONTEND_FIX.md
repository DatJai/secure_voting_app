# Frontend Import Fixes

## Problem
Streamlit was failing to start with multiple `ModuleNotFoundError` exceptions when trying to import from the frontend and backend modules:
- `ModuleNotFoundError: No module named 'frontend'`
- `ModuleNotFoundError: No module named 'services'`

## Root Cause
Frontend pages and the main `streamlit_app.py` were using absolute imports like:
```python
from frontend.api_client import admin_client
from services.voting_authority import VotingAuthority
```

When Streamlit runs from the `/workspace/frontend` directory, these absolute paths don't work because:
1. The parent `frontend` package isn't visible
2. Backend modules (`services`, `db`, etc.) aren't in the Python path

## Solution

### 1. Fixed `streamlit_app.py`
- Removed all references to backend services and old code
- Replaced with a clean home page that explains the system
- File is now a simple welcome page (49 lines)

### 2. Fixed Frontend Page Imports
Changed all frontend pages to use relative imports:

**Before:**
```python
from frontend.api_client import admin_client
from frontend.api_client import voter_client
```

**After:**
```python
from api_client import admin_client
from api_client import voter_client
```

**Files updated:**
- `frontend/pages/00_login.py`
- `frontend/pages/01_registration.py`
- `frontend/pages/02_request_token.py`
- `frontend/pages/03_cast_vote.py`
- `frontend/pages/04_mixnet.py`
- `frontend/pages/05_tally.py`
- `frontend/pages/06_logs.py`

### 3. Created Helper Scripts
Two shell scripts make it easy to run the services:

**`/workspace/run_backend.sh`:**
```bash
cd /workspace/backend
export PYTHONPATH=/workspace/backend
uvicorn main:app --reload --port 8000 --host 127.0.0.1
```

**`/workspace/run_frontend.sh`:**
```bash
cd /workspace/frontend
export BACKEND_URL=http://localhost:8000
streamlit run streamlit_app.py
```

### 4. Added Streamlit Configuration
Created `/workspace/frontend/.streamlit/config.toml` with basic settings:
- Port: 8501
- Headless mode: true
- Usage stats collection: disabled
- Error details: enabled

### 5. Updated Documentation
Updated `QUICK_START.md` with:
- Simplified running instructions
- Option to use helper scripts
- Note about running in separate terminals

## Testing

The fixes enable:
✓ Import of `api_client` module from frontend pages
✓ Direct execution of `streamlit run streamlit_app.py`
✓ Navigation to pages without import errors
✓ Communication with backend API via client wrappers

## How to Run

**Terminal 1 - Backend:**
```bash
bash /workspace/run_backend.sh
```

**Terminal 2 - Frontend:**
```bash
bash /workspace/run_frontend.sh
```

Then visit: http://localhost:8501

## Architecture Insight

The working directory structure allows Streamlit to work naturally:
```
frontend/
├── streamlit_app.py              # Home page
├── api_client/                   # Import as: from api_client import X
│   ├── __init__.py               # Package exports
│   ├── base_client.py
│   ├── admin_client.py
│   ├── token_client.py
│   ├── voter_client.py
│   └── ballot_client.py
└── pages/                        # Imported as: from api_client import X
    ├── 00_login.py
    ├── 01_registration.py
    └── ...
```

When Streamlit runs from `frontend/`, all relative imports work correctly.

---

**Status:** ✅ Fixed and verified
