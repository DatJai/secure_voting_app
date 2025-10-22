# Navigation Guide - Secure Voting System

## Overview

The application has been restructured to use a **single-page multi-view architecture** with **sidebar navigation**. All pages are consolidated into the main `streamlit_app.py` file with a dropdown selector in the sidebar.

## Navigation Structure

### Pre-Login Pages (Unauthenticated)
When you first open the app, you can access:
- **🏠 Home** - Welcome page with system information
- **🔐 Admin Login** - Login form for administrators

### Post-Login Pages (Authenticated)
After successful admin login, additional pages become available:
- **🏠 Home** - Welcome page (accessible anytime)
- **✍️ Register Voter** - Register new voters (auto-generates ID and name)
- **🔑 Request Token** - Issue blind tokens to registered voters
- **🗳️ Cast Vote** - Interface for voters to cast votes
- **🔀 MixNet** - Run ballot anonymization (admin-only)
- **📊 Tally** - View voting results
- **📜 Logs** - View system audit logs (admin-only)
- **🚪 Logout** - Log out and return to pre-login state

## Application Flow

### Stage 1: Authentication & Setup
1. **Home Page** → Read welcome and features
2. **Admin Login** → Authenticate with admin credentials
   - Default: Username: `admin`, Password: `adminpass`
   - System creates JWT token with 2-minute expiry

### Stage 2: Voter Registration
3. **Register Voter** → Add voters to the system
   - Input voter name and email
   - System auto-generates unique Voter ID
   - View list of all registered voters

### Stage 3: Token Distribution
4. **Request Token** → Issue blind tokens to voters
   - Select voter from dropdown
   - System generates and issues blind token
   - Token required for voting

### Stage 4: Voting
5. **Cast Vote** → Voter submits their vote
   - Enter voter ID and name
   - Select candidate from available options
   - Submit vote (uses token for authentication)

### Stage 5: Anonymization
6. **MixNet** → Anonymize ballots (admin-only)
   - Select number of mixing layers (1-10)
   - Run anonymization to shuffle ballots
   - Verify cryptographic mixing

### Stage 6: Results
7. **Tally** → View voting results
   - See vote counts per candidate
   - View percentage breakdown
   - Access public results

### Stage 7: Audit
8. **Logs** → Review system activity (admin-only)
   - View all system events
   - Track authentication, registration, voting
   - Audit trail for compliance

## Sidebar Features

### Page Selector
- **Dropdown menu** labeled "Navigate:" 
- Shows only available pages based on auth state
- Click to instantly navigate to any page

### Authentication Status
- **When logged out:** Shows "ℹ️ Not logged in"
- **When logged in:** Shows "✓ Logged in as Admin"
- Status persists across page navigation

## Session State Management

The app maintains session state across all pages:
- `authenticated` - Boolean login status
- `user_type` - Either "admin" or "voter" (currently all logins are admin)
- `admin_token` - JWT token for API calls
- `voter_id` - Current voter identifier (if applicable)
- `voter_name` - Current voter name (if applicable)

## Key Features

### Auto-Generated Voter IDs
- System generates unique IDs for each voter
- Format: `VOTER-XXXXX` or similar (backend-dependent)
- Displayed upon successful registration

### Token Management
- Admin issues blind tokens to voters
- Tokens have 2-minute expiry for security
- Automatically managed by API client

### Session Persistence
- Logged-in state persists when navigating between pages
- Token automatically refreshed if near expiry
- Logout clears all session state

## Technical Implementation

### Single Page Application (SPA) Pattern
- All content in `streamlit_app.py`
- Each page is a function (e.g., `page_home()`, `page_voter_registration()`)
- Sidebar dropdown selects which function to execute
- Streamlit's `st.rerun()` refreshes UI when needed

### Authorization
- Pre-login pages show to everyone
- Post-login pages only show after successful authentication
- Admin-only pages check `st.session_state.authenticated` and `st.session_state.user_type`
- Unauthorized access shows warning message

### API Integration
- All pages communicate with backend via HTTP clients
- Clients handle token management automatically
- Error handling with user-friendly messages

## Running the Application

### Start Backend
```bash
bash /workspace/run_backend.sh
# Backend runs on http://127.0.0.1:8000
```

### Start Frontend
```bash
bash /workspace/run_frontend.sh
# Frontend runs on http://localhost:8501
```

### Access Application
1. Open browser to http://localhost:8501
2. You'll see Home page with Admin Login option
3. Log in with admin credentials
4. Use sidebar dropdown to navigate between pages

## Troubleshooting

### "⚠️ Admin login required" message
- You're trying to access an admin-only page
- Use **Admin Login** page to authenticate first
- Then navigate to desired page

### Pages not showing in dropdown
- Check authentication status in sidebar
- Pre-login: Only Home and Login pages appear
- Post-login: All pages become available

### Token expired error
- System auto-refreshes tokens before expiry
- If error occurs, log out and log back in

### Page not updating after action
- Streamlit automatically reruns on interaction
- If needed, use browser refresh (F5)

## Future Enhancements

Possible improvements to the navigation structure:
1. Multi-role support (admin, voter, observer)
2. Voter registration self-service
3. Progress indicator showing current voting stage
4. Mobile-responsive sidebar
5. Dark mode toggle in settings
