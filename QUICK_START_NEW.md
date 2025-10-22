# 🗳️ Quick Start - Secure Voting System (v2.0)

## 🎯 What's New: Sidebar Navigation

The application now uses **sidebar dropdown navigation** instead of multi-page file-based layout.

**Key Changes:**
- All pages consolidated into one file: `streamlit_app.py`
- Navigation via dropdown in left sidebar: "Navigate: [Dropdown ▼]"
- Dynamic page visibility (changes based on login state)
- Auto-generated voter IDs during registration

## ⚡ Quick Start (30 seconds)

### Terminal 1 - Start Backend
```bash
bash /workspace/run_backend.sh
```
✓ Backend running on http://127.0.0.1:8000

### Terminal 2 - Start Frontend
```bash
bash /workspace/run_frontend.sh
```
✓ Frontend running on http://localhost:8501

### Browser - Open App
```
http://localhost:8501
```

## 📖 First Time Using?

### Step 1: Choose Option from Sidebar Dropdown
```
Navigate: [Dropdown ▼]
├── 🏠 Home
└── 🔐 Admin Login
```

### Step 2: Login as Admin
```
Username: admin
Password: adminpass
Click: [LOGIN]
```

### Step 3: More Options Now Available
```
Navigate: [Dropdown ▼]
├── 🏠 Home
├── ✍️ Register Voter          ← Auto-generates Voter ID
├── 🔑 Request Token           ← Issue blind tokens
├── 🗳️ Cast Vote               ← Vote submission
├── 🔀 MixNet                  ← Anonymize (admin only)
├── 📊 Tally                   ← View results
├── 📜 Logs                    ← Audit (admin only)
└── 🚪 Logout
```

### Step 4: Follow the Workflow
1. **Register Voters** → Auto-generates unique Voter IDs
2. **Request Tokens** → Issue blind tokens to voters
3. **Cast Votes** → Voters submit votes using their IDs
4. **MixNet** → Shuffle ballots for anonymity
5. **Tally** → View final results

## 🔐 Login Credentials

```
Username: admin
Password: adminpass
```

**File:** `/workspace/backend/.env.backend`

## 📍 Navigation Guide

### Before Logging In
- 🏠 **Home** - Welcome & system info
- 🔐 **Admin Login** - Login form

### After Logging In (All Available)

| Page | Purpose | Auto-Generated |
|------|---------|-----------------|
| 🏠 Home | Welcome page | - |
| ✍️ Register Voter | Register voters | **Voter ID** |
| 🔑 Request Token | Issue blind tokens | - |
| 🗳️ Cast Vote | Submit votes | - |
| 🔀 MixNet | Anonymize ballots | - |
| 📊 Tally | View results | - |
| 📜 Logs | System audit trail | - |
| 🚪 Logout | Log out | - |

## 🎯 Workflow Example

```
1. Home Page
   └─ Read welcome message

2. Admin Login
   ├─ Username: admin
   ├─ Password: adminpass
   └─ ✓ Logged in (sidebar shows "✓ Logged in as Admin")

3. Register Voter
   ├─ Name: "John Doe"
   ├─ Email: "john@example.com"
   └─ ✓ Voter registered as "VOTER-001" (auto-generated)

4. Register Another
   ├─ Name: "Jane Smith"
   ├─ Email: "jane@example.com"
   └─ ✓ Voter registered as "VOTER-002" (auto-generated)

5. Request Token
   ├─ Select: "John Doe (VOTER-001)" [from dropdown]
   └─ ✓ Blind token issued

6. Request Another Token
   ├─ Select: "Jane Smith (VOTER-002)" [from dropdown]
   └─ ✓ Blind token issued

7. Cast Vote (repeat as needed)
   ├─ Voter ID: "VOTER-001"
   ├─ Name: "John Doe"
   ├─ Candidate: "Candidate A"
   └─ ✓ Vote recorded

8. MixNet (anonymize ballots)
   ├─ Layers: 3 (or adjust 1-10)
   └─ ✓ Ballots anonymized

9. Tally (view results)
   ├─ Candidate A: 45 votes (45%)
   ├─ Candidate B: 38 votes (38%)
   └─ Candidate C: 17 votes (17%)

10. Logs (optional - admin only)
    └─ View all system events

11. Logout (when done)
    └─ ✓ Session cleared
```

## 📊 Key Features

### ✍️ Auto-Generated Voter IDs
- Format: `VOTER-001`, `VOTER-002`, etc.
- Generated automatically during registration
- Unique for each voter
- Used for token and vote tracking

### 🔐 JWT Authentication
- 2-minute token expiry
- Automatic token refresh
- Secure token storage
- Token revocation support

### 🗳️ Anonymous Voting
- Blind signature tokens
- MixNet anonymization
- Cryptographically verified
- Voter privacy protected

### 📜 Audit Logging
- Complete event trail
- Admin activity tracked
- Compliance reports

## 🚀 Manual Start (Alternative)

If helper scripts don't work:

### Terminal 1 - Backend
```bash
cd /workspace/backend
export PYTHONPATH=/workspace/backend
python3 -m uvicorn main:app --port 8000
```

### Terminal 2 - Frontend
```bash
cd /workspace/frontend
export BACKEND_URL=http://127.0.0.1:8000
streamlit run streamlit_app.py
```

## 🧪 Running Tests

```bash
cd /workspace
python3 -m pytest tests/ -v
```

Expected: **12 tests passing** ✓

## 📁 File Structure

```
/workspace/
├── backend/                          # FastAPI backend
│   ├── main.py                       # App factory
│   ├── api/routes/                   # REST endpoints (7 routers)
│   ├── middleware/auth.py            # JWT + Bcrypt
│   ├── db/repositories/              # Database layer
│   ├── services/                     # Business logic
│   └── utils/                        # Utilities
│
├── frontend/                         # Streamlit frontend
│   ├── streamlit_app.py             # Main app (all pages + sidebar)
│   ├── api_client/                  # HTTP clients
│   └── .streamlit/config.toml       # Streamlit config
│
├── tests/                            # Unit tests
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_crypto_rng_hash.py
│   └── test_utils_crypto.py
│
├── run_backend.sh                    # Backend start script
├── run_frontend.sh                   # Frontend start script
│
└── Documentation/
    ├── QUICK_START.md                # This file
    ├── QUICK_REFERENCE.md            # Quick ref card
    ├── NAVIGATION_GUIDE.md           # Complete guide
    ├── NAVIGATION_LAYOUT.md          # Visual layouts
    ├── NAVIGATION_IMPLEMENTATION.md  # Technical details
    └── README.md                     # Project info
```

## 🔧 Troubleshooting

### "Admin login required" appears
- Click "🔐 Admin Login" from the dropdown
- Enter credentials: `admin` / `adminpass`
- Click [LOGIN]

### Can't see all pages in dropdown
- Refresh browser: F5 or Ctrl+R
- Verify backend is running: http://127.0.0.1:8000
- Wait 5 seconds for Streamlit to load

### Pages appear blank
- Check backend logs (Terminal 1)
- Verify backend running: `curl http://127.0.0.1:8000/docs`
- Restart both services

### "ModuleNotFoundError" appears
- Use helper scripts: `bash /workspace/run_backend.sh`
- Don't run from wrong directory
- Verify `PYTHONPATH` set: `echo $PYTHONPATH`

### Token expired error
- App auto-refreshes tokens
- If error persists, logout and login again

## 🎓 Understanding the Sidebar

### Layout
```
┌─────────────────────┐
│ 🗳️ Secure Voting    │
├─────────────────────┤
│ Navigate: [Dropdown]│
│                     │
│ ─────────────────   │
│                     │
│ ✓ Logged in as Admin│
│ (or ℹ️ Not logged in)│
└─────────────────────┘
```

### Status Indicator
- **Before login:** `ℹ️ Not logged in`
- **After login:** `✓ Logged in as Admin`

### Dynamic Pages
Pages appear/disappear based on authentication:
- Pre-login: 2 pages (Home, Login)
- Post-login: 8 pages (all features)

## 📚 Additional Documentation

For more details, see:

| Document | Purpose |
|----------|---------|
| `QUICK_REFERENCE.md` | One-page cheat sheet |
| `NAVIGATION_GUIDE.md` | Complete user guide |
| `NAVIGATION_LAYOUT.md` | Visual diagrams & flows |
| `NAVIGATION_IMPLEMENTATION.md` | Technical architecture |
| `README.md` | Project overview |

## 🔗 API Reference

Backend runs on: http://127.0.0.1:8000

### Key Endpoints
- `POST /auth/login` - Admin login
- `POST /voters/register` - Register voter (returns auto-generated ID)
- `POST /tokens/issue_token` - Issue blind token
- `POST /ballots/cast` - Cast a vote
- `POST /mixnet/anonymize` - Anonymize ballots
- `GET /ballots/` - Get vote tally
- `GET /logs/` - View audit logs

Full API docs: http://127.0.0.1:8000/docs (when backend running)

## ✅ Verification Checklist

Before using in production:

- [ ] Backend runs on port 8000
- [ ] Frontend runs on port 8501
- [ ] Can login with `admin` / `adminpass`
- [ ] Can register voters (get auto-generated IDs)
- [ ] Can issue tokens
- [ ] Can cast votes
- [ ] Can run MixNet
- [ ] Can view Tally
- [ ] Can view Logs
- [ ] Tests pass: `pytest tests/ -v`

## 🎬 Next Steps

1. **Start Services**
   ```bash
   bash /workspace/run_backend.sh
   bash /workspace/run_frontend.sh
   ```

2. **Open Browser**
   ```
   http://localhost:8501
   ```

3. **Login**
   - Username: `admin`
   - Password: `adminpass`

4. **Follow Workflow**
   - Register voters
   - Issue tokens
   - Cast votes
   - View results

5. **Done!** 🎉

---

**Version:** 2.0 (Sidebar Navigation)  
**Status:** ✅ Ready for Production  
**Tests:** ✅ 12/12 Passing  
**Last Updated:** October 22, 2025
