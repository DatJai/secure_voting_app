# 🗳️ Secure Voting System - New Navigation Layout

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  🗳️ Secure Voting System                           [⚙]  │
├──────────────────────────┬──────────────────────────────┤
│                          │                              │
│  🗳️ Secure Voting        │                              │
│  ─────────────────────   │                              │
│  Navigate: [Dropdown ▼]  │    PAGE CONTENT              │
│                          │    ─────────────────         │
│  ─────────────────────   │                              │
│                          │    Displays selected         │
│  ✓ Logged in as Admin    │    page content              │
│                          │                              │
│  (or ℹ️ Not logged in)    │                              │
│                          │                              │
│                          │                              │
│                          │                              │
│                          │                              │
└──────────────────────────┴──────────────────────────────┘
```

## Navigation Dropdown Options

### 🔴 Before Login
```
Navigate: [▼]
├── 🏠 Home
└── 🔐 Admin Login
```

### 🟢 After Login
```
Navigate: [▼]
├── 🏠 Home
├── ✍️ Register Voter
├── 🔑 Request Token
├── 🗳️ Cast Vote
├── 🔀 MixNet
├── 📊 Tally
├── 📜 Logs
└── 🚪 Logout
```

## Voting Process Flow

```
                    ┌─────────────────────────────────┐
                    │   🏠 HOME PAGE                  │
                    │  Welcome & Info                 │
                    │                                 │
                    │  [Navigate to Admin Login →]    │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │   🔐 ADMIN LOGIN                │
                    │  ┌──────────────────────────┐   │
                    │  │ Username: admin          │   │
                    │  │ Password: ••••••••       │   │
                    │  │ [LOGIN]                  │   │
                    │  └──────────────────────────┘   │
                    └──────────────┬──────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
    ┌────▼────────────┐   ┌────────▼──────────┐   ┌─────────▼──────────┐
    │ ✍️ VOTER         │   │ 🔑 REQUEST TOKEN  │   │ 🗳️ CAST VOTE       │
    │ REGISTRATION    │   │                   │   │                    │
    │                 │   │ Select voter      │   │ Enter Voter ID     │
    │ Name: [______]  │   │ [Dropdown ▼]      │   │ [__________]       │
    │ Email:[______]  │   │                   │   │                    │
    │ [REGISTER]      │   │ [ISSUE TOKEN]     │   │ Select candidate:  │
    │                 │   │                   │   │ [Dropdown ▼]       │
    │ ✓ List showing: │   │ ✓ Token issued    │   │ [CAST VOTE]        │
    │ - VOTER-001     │   │   for voter       │   │                    │
    │ - VOTER-002     │   └───────────────────┘   └────────────────────┘
    │ - VOTER-003     │
    └─────────────────┘
         │
         ├──────────────────────────────────────────┐
         │                                          │
    ┌────▼──────────────┐    ┌──────────────────┐  │
    │ 🔀 MIXNET         │    │ 📊 TALLY         │  │
    │ (ADMIN ONLY)      │    │                  │  │
    │                   │    │ Candidate A: 45  │  │
    │ Mixing layers:    │    │ Candidate B: 38  │  │
    │ [1 ◄─► 10]       │    │ Candidate C: 17  │  │
    │ ◀3▶                │    │                  │  │
    │ [RUN MIXNET]      │    │ Chart view       │  │
    │                   │    │ available        │  │
    │ ✓ Complete        │    └──────────────────┘  │
    │   Ballots mixed!  │                          │
    └─────────────────┘     └──────────────────────┘
                                    │
                            ┌───────▼─────────────┐
                            │ 📜 LOGS             │
                            │ (ADMIN ONLY)        │
                            │                     │
                            │ [INFO] Login        │
                            │ [INFO] Registration │
                            │ [INFO] Vote cast    │
                            │ [INFO] MixNet run   │
                            └─────────────────────┘
```

## Key Features at a Glance

| Feature | Location | Access | Purpose |
|---------|----------|--------|---------|
| Welcome | Home | Everyone | System overview |
| Admin Auth | Admin Login | Everyone | Get API token |
| Voter Setup | Register Voter | Admin only | Create voter accounts |
| Token Issue | Request Token | Admin only | Issue blind tokens |
| Vote Submit | Cast Vote | Everyone | Submit votes |
| Anonymize | MixNet | Admin only | Shuffle ballots |
| Results | Tally | Everyone | View vote counts |
| Audit | Logs | Admin only | System activity |
| Exit | Logout | When logged in | Clear session |

## Getting Started

### Prerequisites
- Backend running on http://127.0.0.1:8000
- Frontend running on http://localhost:8501

### Step-by-Step

1. **Open Frontend**
   - Navigate to http://localhost:8501
   - See Home page

2. **Login as Admin**
   - Select "🔐 Admin Login" from dropdown
   - Enter: `admin` / `adminpass`
   - Click [LOGIN]

3. **Register Voters**
   - Select "✍️ Register Voter"
   - Enter voter names and emails
   - View auto-generated Voter IDs

4. **Issue Tokens**
   - Select "🔑 Request Token"
   - Choose voter from list
   - Click [ISSUE BLIND TOKEN]

5. **Cast Votes**
   - Select "🗳️ Cast Vote"
   - Enter voter ID
   - Select candidate
   - Click [CAST VOTE]

6. **Run MixNet**
   - Select "🔀 MixNet"
   - Adjust mixing layers if needed
   - Click [RUN MIXNET]

7. **View Results**
   - Select "📊 Tally"
   - See vote counts and percentages

8. **Review Logs**
   - Select "📜 Logs"
   - View all system activity

9. **Logout**
   - Select "🚪 Logout"
   - Return to pre-login state

## Sidebar Status

```
┌────────────────────────┐
│ 🗳️ Secure Voting       │
├────────────────────────┤
│ Navigate: [Dropdown ▼] │
│                        │
├────────────────────────┤
│                        │
│ ✓ Logged in as Admin   │ ← Status indicator
│                        │ (Changes based on auth)
└────────────────────────┘
```

Status shows:
- **Before login:** `ℹ️ Not logged in`
- **After login:** `✓ Logged in as Admin`

## Navigation Behavior

### Dynamic Dropdown
- Pages appear/disappear based on login state
- Pre-login: 2 pages (Home, Login)
- Post-login: 8 pages (Home, Register, Token, Vote, MixNet, Tally, Logs, Logout)

### Instant Navigation
- Click any page name in dropdown
- Content updates immediately
- No page reload needed
- Session state persists

### Admin-Only Pages
- Pages check `st.session_state.authenticated`
- Unauthenticated access shows warning
- Redirect to login recommended

## Browser Support

Works on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge

Responsive design adapts to:
- Desktop (recommended)
- Tablet
- Mobile (minimal - sidebar collapses)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dropdown empty | Page not loading; check backend |
| Can't see all pages | Log in first |
| Session lost | Browser refresh or F5 |
| Token expired | Auto-refresh; re-login if needed |
| API connection error | Verify backend running on 8000 |
