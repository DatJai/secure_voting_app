# Quick Start Guide

## Project Structure Summary

### Backend (FastAPI + JWT Auth)
```
backend/
├── main.py                          # FastAPI app with routers
├── .env.backend                     # Config (JWT_SECRET, DB_URL, admin creds)
├── api/
│   ├── models/                      # Pydantic models
│   ├── routes/                      # FastAPI routers
│   │   ├── auth.py                  # /auth/* endpoints
│   │   ├── users.py                 # /users/* (admin only)
│   │   ├── voters.py                # /voters/*
│   │   ├── tokens.py                # /tokens/*
│   │   ├── ballots.py               # /ballots/*
│   │   ├── mixnet.py                # /mixnet/* (admin only)
│   │   └── logs.py                  # /logs/*
│   └── middleware/
│       └── auth.py                  # JWT verify, bcrypt, revocation
├── db/
│   ├── repositories/                # DB access layer
│   │   ├── user_repository.py       # NEW: User CRUD + auth
│   │   └── revoked_token_repository.py  # NEW: Token blacklist
│   └── connection.py
└── services/                        # Business logic (RSA, mixnet, voting)
```

### Frontend (Streamlit + API Client)
```
frontend/
├── api_client/                      # NEW: HTTP API wrappers
│   ├── __init__.py                  # Exports: base_client, admin_client, ...
│   ├── base_client.py               # Session, tokens, auto-refresh
│   ├── admin_client.py              # Login, user mgmt, mixnet
│   ├── token_client.py              # Blind token workflow
│   ├── voter_client.py              # Voter registration
│   └── ballot_client.py             # Vote casting
├── streamlit_app.py                 # Main entry (mostly commented out)
└── pages/
    ├── 00_login.py                  # NEW: Admin login page
    ├── 01_registration.py           # Uses voter_client
    ├── 02_request_token.py          # Uses token_client
    ├── 03_cast_vote.py              # Uses ballot_client
    ├── 04_mixnet.py                 # Uses admin_client (admin only)
    ├── 05_tally.py                  # Uses ballot_client
    └── 06_logs.py                   # Uses base_client
```

## Running the Application

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 2. Set Up Backend Environment
```bash
cd backend
# Already has .env.backend with JWT_SECRET and admin credentials
```

### 3. Start Backend API
```bash
cd /workspace/backend
PYTHONPATH=/workspace/backend uvicorn main:app --reload --port 8000 --host 127.0.0.1
```

Or use the provided script:
```bash
bash /workspace/run_backend.sh
```

### 4. Start Frontend (in another terminal)
```bash
cd /workspace/frontend
export BACKEND_URL=http://localhost:8000
streamlit run streamlit_app.py
```

Or use the provided script:
```bash
bash /workspace/run_frontend.sh
```

**Note:** Make sure to run these commands from separate terminals so both services can run simultaneously.

## Authentication Flow

1. **Admin Login**

```   - Visit `http://localhost:8501/00_login`
   - Enter credentials (default: `admin` / from `.env.backend`)
   - Token stored in `st.session_state` + requests Session

2. **Token Auto-Refresh**
   - When token expires (2 minutes), BaseClient auto-refreshes via `/auth/refresh`
   - No manual intervention needed

3. **Protected Endpoints**
   - All `/admin/*`, `/users/*`, `/auth/revoke` require valid token
   - Authorization header: `Bearer <token>`

## Key Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/auth/token` | None | Login (admin) |
| POST | `/auth/refresh` | Token | Refresh access token |
| POST | `/auth/revoke` | Token | Revoke current token |
| POST | `/users/register` | Admin | Create new admin user |
| GET | `/users/` | Admin | List all users |
| POST | `/voters/register` | None | Register voter |
| GET | `/voters/` | None | List voters |
| GET | `/tokens/public_key` | None | Get RSA public key |
| POST | `/tokens/issue` | None | Issue blind signature |
| GET | `/tokens/by_voter/{id}` | None | Get voter's tokens |
| POST | `/ballots/cast` | None | Submit encrypted vote |
| GET | `/ballots/` | None | List ballots |
| POST | `/mixnet/run` | Admin | Run anonymization |
| GET | `/logs/` | Admin | Fetch audit logs |

## Environment Variables

### Backend (`backend/.env.backend`)
```
DATABASE_URL=postgresql://user:password@localhost/voting_db
JWT_SECRET=<generated-secret-key>
JWT_EXPIRE_MINUTES=2
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<secure-password>
```

### Frontend (optional `.streamlit/secrets.toml` or env)
```
BACKEND_URL=http://localhost:8000
```

## Testing

Run all tests:
```bash
cd /workspace
PYTHONPATH=/workspace:/workspace/backend pytest -q tests/
# Result: 12 passed
```

Test specific module:
```bash
PYTHONPATH=/workspace:/workspace/backend pytest -q tests/test_auth.py -v
```

## Common Tasks

### Create Admin User via API
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "newadmin", "password": "secure_pass"}'
```

### Register a Voter
```bash
curl -X POST http://localhost:8000/voters/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Get Public Key for Blinding
```bash
curl http://localhost:8000/tokens/public_key | jq .
```

### Cast a Vote
```bash
curl -X POST http://localhost:8000/ballots/cast \
  -H "Content-Type: application/json" \
  -d '{"voter_id": "voter123", "token": "token_hex", "vote": {"candidate": "Candidate A"}}'
```

## Troubleshooting

**ModuleNotFoundError: No module named 'backend'**
- Set `PYTHONPATH=/workspace:/workspace/backend` before running tests/python

**ConnectionRefusedError: Cannot connect to backend**
- Ensure backend is running on port 8000
- Check `BACKEND_URL` is correct in frontend

**Token expired error in Streamlit**
- BaseClient auto-refreshes tokens; if still failing, logout and login again

**Database connection errors**
- Check `DATABASE_URL` in `backend/.env.backend`
- PostgreSQL must be running (tests use in-memory fallbacks)

## Architecture Highlights

✅ **Separation of Concerns**
- Backend: REST API + auth logic
- Frontend: Streamlit UI + HTTP client wrappers

✅ **Security**
- JWT tokens with 2-minute expiry
- Bcrypt password hashing
- Token revocation/blacklist
- Protected admin endpoints

✅ **Scalability**
- Stateless JWT (no session storage needed)
- Database-backed user & revocation tables
- MixNet anonymization for votes

✅ **Testability**
- 12 unit tests covering auth, users, crypto
- DB fallbacks for local testing
- pytest configuration in `pytest.ini`

---

**For detailed integration info, see:** `FRONTEND_INTEGRATION.md`
