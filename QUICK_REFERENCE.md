# 🎯 Quick Reference - New Navigation

## Start Voting System

```bash
# Terminal 1 - Backend
bash /workspace/run_backend.sh

# Terminal 2 - Frontend  
bash /workspace/run_frontend.sh

# Browser
Open: http://localhost:8501
```

## Login
```
Username: admin
Password: adminpass
```

## Navigation Menu

### Sidebar Dropdown: Navigate →

**Before Login:**
- 🏠 Home
- 🔐 Admin Login

**After Login:**
- 🏠 Home
- ✍️ Register Voter
- 🔑 Request Token
- 🗳️ Cast Vote
- 🔀 MixNet (admin)
- 📊 Tally
- 📜 Logs (admin)
- 🚪 Logout

## Flow Steps

```
1. Open Frontend → Home Page
   └─ See: Welcome, Features, Getting Started

2. Click: 🔐 Admin Login
   ├─ Enter: admin / adminpass
   ├─ Click: LOGIN
   └─ Result: ✓ Logged in as Admin (shows in sidebar)

3. Click: ✍️ Register Voter
   ├─ Enter: Name & Email
   ├─ Click: REGISTER VOTER
   ├─ See: Auto-generated Voter ID
   └─ Repeat: Register multiple voters

4. Click: 🔑 Request Token
   ├─ Select: Voter from dropdown
   ├─ Click: ISSUE BLIND TOKEN
   └─ Result: Token issued for voter

5. Click: 🗳️ Cast Vote
   ├─ Enter: Voter ID & Name
   ├─ Select: Candidate
   ├─ Click: CAST VOTE
   └─ Result: Vote recorded

6. Click: 🔀 MixNet
   ├─ Adjust: Mixing layers (1-10)
   ├─ Click: RUN MIXNET
   └─ Result: ✓ Ballots anonymized

7. Click: 📊 Tally
   ├─ See: Vote counts per candidate
   ├─ See: Percentage breakdown
   └─ View: Final results

8. (Admin only) Click: 📜 Logs
   ├─ See: All system events
   ├─ Filter: By type (optional)
   └─ Audit: Check compliance

9. Click: 🚪 Logout
   └─ Result: Back to pre-login state
```

## Page Features

| Page | Admin Only | Auto-Generated | Input | Output |
|------|-----------|-----------------|-------|--------|
| Home | ❌ | - | - | Info only |
| Login | ❌ | - | Credentials | Token |
| Register | ✅ | **Voter ID** | Name, Email | Confirmation |
| Token | ✅ | - | Select Voter | Token |
| Vote | ❌ | - | ID, Name, Choice | Receipt |
| MixNet | ✅ | - | Layers | Anon. Status |
| Tally | ❌ | - | - | Results |
| Logs | ✅ | - | - | Events |

## Key Points

### Auto-Generated Voter IDs
- Generated automatically during registration
- Format: `VOTER-001`, `VOTER-002`, etc.
- Unique per voter
- Used for token and vote linking

### Two Stages

**Stage 1: Authentication & Setup**
- Login as admin
- Register voters with auto-generated IDs
- Issue blind tokens

**Stage 2: Voting**
- Cast votes (anyone can enter voter info)
- MixNet anonymizes (admin-only)
- View results (everyone)

### Session Persistence
- Logged-in state persists when navigating
- Token auto-refreshes before expiry
- Logout clears all session data

### Admin-Only Pages
- ✍️ Register Voter
- 🔑 Request Token
- 🔀 MixNet
- 📜 Logs
- 🚪 Logout (only when logged in)

Show warning if accessed without login:
> ⚠️ Admin login required. Please log in first.

## Sidebar Info

```
╔══════════════════════════════╗
║ 🗳️ Secure Voting            ║
╠══════════════════════════════╣
║ Navigate: [Dropdown ▼]       ║
║                              ║
╠══════════════════════════════╣
║                              ║
║ ✓ Logged in as Admin         ║
║ (or ℹ️ Not logged in)         ║
║                              ║
╚══════════════════════════════╝
```

## Files Location

| File | Purpose |
|------|---------|
| `/workspace/frontend/streamlit_app.py` | Main app |
| `/workspace/frontend/api_client/` | HTTP clients |
| `/workspace/run_frontend.sh` | Start script |
| `/workspace/run_backend.sh` | Backend start |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't see pages | Click "🔐 Admin Login" first |
| Can't login | Check credentials (admin/adminpass) |
| API error | Verify backend running (port 8000) |
| Session lost | This is normal - log in again |
| Page blank | Refresh browser (F5) |
| Dropdown empty | Wait for load (~5 sec) |

## Environment

```
Backend: http://127.0.0.1:8000
Frontend: http://localhost:8501
Admin User: admin
Admin Pass: adminpass
Token Expiry: 2 minutes
```

## Architecture

```
Frontend (Streamlit)
    ├── Sidebar Navigation
    │   └── Dropdown: Navigate →
    │
    ├── Pages (functions)
    │   ├── page_home()
    │   ├── page_admin_login()
    │   ├── page_voter_registration()
    │   ├── page_request_token()
    │   ├── page_cast_vote()
    │   ├── page_mixnet()
    │   ├── page_tally()
    │   ├── page_logs()
    │   └── page_logout()
    │
    └── API Clients
        ├── admin_client
        ├── voter_client
        ├── token_client
        ├── ballot_client
        └── base_client
        
            ↓ HTTP ↓
            
Backend (FastAPI)
    ├── /auth/* (login, refresh, revoke)
    ├── /users/* (admin user management)
    ├── /voters/* (registration, listing)
    ├── /tokens/* (blind token workflow)
    ├── /ballots/* (voting, listing)
    ├── /mixnet/* (anonymization)
    └── /logs/* (audit trail)
        
            ↓ DB ↓
            
PostgreSQL (or in-memory fallback)
    ├── users
    ├── voters
    ├── tokens
    ├── ballots
    ├── logs
    └── revoked_tokens
```

## Document Reference

- 📖 `NAVIGATION_GUIDE.md` - Full user guide
- 🎨 `NAVIGATION_LAYOUT.md` - Visual diagrams
- ⚙️ `NAVIGATION_IMPLEMENTATION.md` - Technical details
- 📋 `QUICK_REFERENCE.md` - This file

## Next Steps

1. ✅ Ensure backend is running
2. ✅ Start frontend
3. ✅ Open http://localhost:8501
4. ✅ Follow the flow steps above
5. ✅ Enjoy secure voting!

---

**Last Updated:** Oct 22, 2025  
**Status:** Ready for Deployment  
**Version:** 2.0 (Sidebar Navigation)
