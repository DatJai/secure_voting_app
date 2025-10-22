# Frontend API Integration Summary

## Overview
The frontend has been updated to communicate with the backend REST API via a set of lightweight HTTP client wrappers instead of direct database/service access. All Streamlit pages now use the new `frontend.api_client` module for backend communication.

## Changes Made

### 1. Frontend API Clients (`frontend/api_client/`)
All clients built on top of `BaseClient` which handles:
- Session management with `requests`
- Token storage and auto-refresh on 401 responses
- Automatic Authorization header injection
- Base URL configuration via `BACKEND_URL` env var

**Implemented clients:**

- **`base_client.py`** — Core HTTP wrapper
  - Methods: `get()`, `post()`, `put()`, `delete()`
  - Token management: `set_tokens()`, `get_tokens()`
  - Auto-refresh on 401 via `/auth/refresh` endpoint

- **`admin_client.py`** — Admin operations
  - `login(username, password)` — OAuth2 password grant → stores tokens in session
  - `create_user(username, password, scopes)` — Register new admin user
  - `list_users()` — Fetch all users (admin only)
  - `revoke_current()` — Revoke own token
  - `run_mixnet(layers)` — Run anonymization (admin only)

- **`token_client.py`** — Blind token workflow
  - `public_key()` — Fetch RSA public key for blinding
  - `issue_token(voter_id, blinded_message)` — Issue blind signature
  - `tokens_by_voter(voter_id)` — Retrieve tokens for a voter

- **`voter_client.py`** — Voter management
  - `register(name, email)` — Register new voter
  - `list()` — Fetch all voters

- **`ballot_client.py`** — Ballot casting
  - `cast(voter_id, token, vote)` — Submit encrypted vote
  - `list()` — Retrieve all ballots

### 2. Streamlit Pages Updated

- **`pages/00_login.py`** (NEW)
  - Admin login page
  - Stores `admin_token` and `admin_username` in `st.session_state`
  - Logout with token revocation support

- **`pages/01_registration.py`**
  - Now uses `voter_client.register()` and `voter_client.list()`
  - Replaced direct DB access with HTTP calls

- **`pages/02_request_token.py`**
  - Uses `token_client.public_key()` and `token_client.issue_token()`
  - Fetches eligible voters via `voter_client.list()`

- **`pages/03_cast_vote.py`**
  - Uses `ballot_client.cast()` to submit votes
  - Fetches voter eligibility and tokens via `voter_client.list()` and `token_client.tokens_by_voter()`

- **`pages/04_mixnet.py`**
  - Admin-protected via `st.session_state.admin_token` check
  - Uses `admin_client.run_mixnet()`

- **`pages/05_tally.py`**
  - Uses `ballot_client.list()` to fetch ballots
  - Tallies results client-side

- **`pages/06_logs.py`**
  - Uses `base_client.get("/logs/")` to fetch logs

### 3. Configuration

**Environment Variables Required:**
```bash
BACKEND_URL=http://localhost:8000  # Backend server URL (set in frontend)
JWT_SECRET=<generated-secret>       # Backend token signing key
JWT_EXPIRE_MINUTES=2                # Token expiry (backend)
ADMIN_USERNAME=admin                # Default admin user
ADMIN_PASSWORD=<password>           # Default admin password
DATABASE_URL=postgresql://...       # Backend DB connection (optional for local dev)
```

**File: `backend/.env.backend`**
- Pre-configured with `JWT_SECRET`, expiry, and admin credentials
- Copy settings to frontend env as needed

## Testing

**All tests pass:**
```bash
PYTHONPATH=/workspace:/workspace/backend pytest -q tests/
# Result: 12 passed in 2.65s
```

**Frontend imports verified:**
```bash
PYTHONPATH=/workspace:/workspace/backend python3 -c "
  from frontend.api_client import base_client, admin_client, token_client, voter_client, ballot_client
  print('✓ All frontend clients imported successfully')
"
```

## Usage Flow

### 1. Admin Login
```python
from frontend.api_client import admin_client
result = admin_client.login("admin", "password")
# Tokens automatically stored in BaseClient.session_state
```

### 2. Register Voter
```python
from frontend.api_client import voter_client
result = voter_client.register(name="Alice", email="alice@example.com")
```

### 3. Issue Blind Token
```python
from frontend.api_client import token_client
pk = token_client.public_key()
token_result = token_client.issue_token(voter_id="voter123", blinded_message="...")
```

### 4. Cast Vote
```python
from frontend.api_client import ballot_client
ballot = ballot_client.cast(
    voter_id="voter123",
    token="token_hex",
    vote={"candidate": "Candidate A"}
)
```

### 5. Run Mixnet (Admin Only)
```python
from frontend.api_client import admin_client
result = admin_client.run_mixnet(layers=3)
```

## Key Features

✓ **Stateless JWT Auth** — 2-minute expiry tokens; auto-refresh on 401
✓ **Token Revocation** — Admin can revoke tokens; checked on every request
✓ **Minimal Streamlit Changes** — Direct DB/service calls replaced with HTTP; no complex state management
✓ **Error Handling** — Try/except blocks in all pages; user-friendly error messages
✓ **Session State** — Admin tokens stored in `st.session_state` for persistence across reruns

## Backend Endpoints Called

| Endpoint | Client | Purpose |
|----------|--------|---------|
| `/auth/token` | `admin_client` | Login (OAuth2 password grant) |
| `/auth/refresh` | `base_client` | Auto-refresh tokens |
| `/auth/revoke` | `admin_client` | Revoke current token |
| `/users/register` | `admin_client` | Create admin user |
| `/users/` | `admin_client` | List users |
| `/voters/register` | `voter_client` | Register voter |
| `/voters/` | `voter_client` | List voters |
| `/tokens/public_key` | `token_client` | Get RSA public key |
| `/tokens/issue` | `token_client` | Issue blind signature |
| `/tokens/by_voter/{id}` | `token_client` | Get voter tokens |
| `/ballots/cast` | `ballot_client` | Submit vote |
| `/ballots/` | `ballot_client` | List ballots |
| `/mixnet/run` | `admin_client` | Run anonymization |
| `/logs/` | `base_client` | Fetch logs |

## Next Steps (Optional)

- [ ] Add `BACKEND_URL` env var support in Streamlit (via `st.secrets` or `.streamlit/secrets.toml`)
- [ ] Add loading spinners during API calls for better UX
- [ ] Implement token refresh UI feedback
- [ ] Add logout button on main pages (currently only in login page)
- [ ] Deploy frontend and backend separately (update `BACKEND_URL` in production)
- [ ] Add rate limiting and exponential backoff for retries
- [ ] Integrate with a proper secrets management system (e.g., Vault, AWS Secrets Manager)

## Files Modified/Created

```
frontend/
├── api_client/
│   ├── __init__.py (updated with exports)
│   ├── base_client.py (new)
│   ├── admin_client.py (new)
│   ├── token_client.py (new)
│   ├── voter_client.py (new)
│   └── ballot_client.py (new)
└── pages/
    ├── 00_login.py (new)
    ├── 01_registration.py (updated)
    ├── 02_request_token.py (updated)
    ├── 03_cast_vote.py (updated)
    ├── 04_mixnet.py (updated)
    ├── 05_tally.py (updated)
    └── 06_logs.py (updated)

backend/
├── .env.backend (contains JWT_SECRET, credentials)
├── main.py (all routers mounted)
├── api/
│   ├── models/ (voter, token, ballot, response, user)
│   └── routes/ (voters, tokens, ballots, mixnet, logs, auth, users)
├── middleware/
│   └── auth.py (JWT, bcrypt, revocation)
└── db/
    └── repositories/ (+ user_repository.py, revoked_token_repository.py)

tests/
├── test_auth.py
├── test_users.py
└── ... (others passing)

pytest.ini (new - configures PYTHONPATH)
```

---

**Status:** ✅ All tasks completed. Backend API fully integrated with frontend. All tests passing.
