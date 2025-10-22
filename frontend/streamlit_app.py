import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables early
env_path = Path(__file__).parent / ".env.frontend"
load_dotenv(dotenv_path=env_path)

# Fallback to .env if .env.frontend not found
if not os.getenv("BACKEND_URL"):
    load_dotenv()

# Configure page
st.set_page_config(
    page_title="Secure Voting System",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None  # "admin" or "voter"
if "admin_token" not in st.session_state:
    st.session_state.admin_token = None
if "voter_id" not in st.session_state:
    st.session_state.voter_id = None
if "voter_name" not in st.session_state:
    st.session_state.voter_name = None

# Import clients
from api_client import admin_client, voter_client, token_client, ballot_client, base_client

# ===== PAGES =====

def page_home():
    """Home page with system information"""
    st.title("🗳️ Secure Voting System")
    st.markdown("""
    ## Welcome to the Secure Voting Platform
    
    A transparent, secure, and accessible voting system for the digital age.
    
    ### Features
    - 🔐 **Secure Authentication** — JWT-based with 2-minute token expiry
    - 🗳️ **Anonymous Voting** — Blind signatures and token-based voting
    - 🔀 **MixNet Anonymization** — Verifiable shuffling of ballots
    - 📊 **Transparent Tallying** — Cryptographically verifiable results
    - ⚡ **Real-time Updates** — Live voting and result tracking
    
    ### How It Works
    1. **Register Account** — Create voter account or login as admin
    2. **Admin Setup** — Admins register voters and manage system
    3. **Token Request** — Voters request blind tokens
    4. **Vote Casting** — Voters cast votes anonymously
    5. **MixNet** — Ballots are anonymized via mixing
    6. **Tally** — Final results are computed and displayed
    
    ---
    
    **Status:** Ready to vote  
    **Backend:** API running on http://localhost:8000  
    **Choose an option from the sidebar to begin →**
    """)

def page_register_voter():
    """Voter self-registration page (pre-login)"""
    st.title("📝 Create Voter Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("Create a new voter account to participate in the voting system.")
        
        with st.form("voter_register_form"):
            voter_name = st.text_input("Full Name", placeholder="e.g., John Doe")
            voter_email = st.text_input("Email Address", placeholder="e.g., john@example.com")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if not voter_name or not voter_email:
                    st.error("✗ Please enter both name and email.")
                else:
                    try:
                        result = voter_client.register(voter_name, voter_email)
                        st.success("✓ Account created successfully!")
                        st.info(f"Your Voter ID: **{result.get('id', 'VOTER-XXX')}**")
                        st.write("You can now login as a voter with this system.")
                    except Exception as e:
                        st.error(f"✗ Registration failed: {str(e)}")

def page_admin_login():
    """System access page - Admin and Voter login"""
    st.title("🔐 System Access")
    
    # Create tabs for Admin vs Voter login
    tab1, tab2 = st.tabs(["👨‍💼 Admin Login", "🗳️ Voter Login"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("**Admin System Access**")
            st.write("Enter admin credentials to manage the voting system.")
            
            with st.form("admin_login_form"):
                username = st.text_input("Username", value="admin", key="admin_user")
                password = st.text_input("Password", type="password", value="adminpass", key="admin_pass")
                submitted = st.form_submit_button("Login as Admin", use_container_width=True)
                
                if submitted:
                    try:
                        result = admin_client.login(username, password)
                        st.session_state.authenticated = True
                        st.session_state.user_type = "admin"
                        st.session_state.admin_token = result.get("access_token")
                        st.session_state.voter_id = None
                        st.session_state.voter_name = None
                        st.success("✓ Admin login successful!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"✗ Admin login failed: {str(e)}")
    
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("**Voter System Access**")
            st.write("Enter your voter credentials to cast your vote.")
            
            with st.form("voter_login_form"):
                voter_id = st.text_input("Your Voter ID", placeholder="e.g., VOTER-001", key="voter_id_login")
                voter_name = st.text_input("Your Name", placeholder="e.g., John Doe", key="voter_name_login")
                submitted = st.form_submit_button("Login as Voter", use_container_width=True)
                
                if submitted:
                    if not voter_id or not voter_name:
                        st.error("✗ Please enter both Voter ID and Name.")
                    else:
                        # Verify voter exists
                        try:
                            voters = voter_client.list()
                            voter_list = voters.get("voters", [])
                            voter_found = any(v.get("id") == voter_id for v in voter_list)
                            
                            if voter_found:
                                st.session_state.authenticated = True
                                st.session_state.user_type = "voter"
                                st.session_state.voter_id = voter_id
                                st.session_state.voter_name = voter_name
                                st.session_state.admin_token = None
                                st.success(f"✓ Welcome, {voter_name}!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"✗ Voter ID '{voter_id}' not found. Please register first.")
                        except Exception as e:
                            st.error(f"✗ Voter login failed: {str(e)}")

def page_voter_registration():
    """Voter registration page (admin & voter can access)"""
    st.title("✍️ Register New Voter")
    
    # Allow both admin and voter to access
    if not st.session_state.authenticated:
        st.warning("⚠️ Login required. Please log in first.")
        return
    
    # Determine user context
    if st.session_state.user_type == "admin":
        context_msg = "**Admin Function:** Register a new voter. Voter ID and name will be auto-generated."
    else:  # voter
        context_msg = "**Self-Register:** Create a new voter account. Voter ID will be auto-generated."
    
    st.write(context_msg)
    
    col1, col2 = st.columns(2)
    with col1:
        voter_name = st.text_input("Voter Name", placeholder="e.g., John Doe")
    with col2:
        voter_email = st.text_input("Voter Email", placeholder="e.g., john@example.com")
    
    if st.button("Register Voter", use_container_width=True, key="register_voter_btn"):
        if not voter_name or not voter_email:
            st.error("✗ Please enter both name and email.")
        else:
            try:
                result = voter_client.register(voter_name, voter_email)
                st.success(f"✓ Voter registered successfully!")
                st.info(f"Generated Voter ID: **{result.get('id', 'VOTER-XXX')}**")
                if st.session_state.user_type == "voter":
                    st.write("This voter can now login with the generated Voter ID.")
                st.json(result)
            except Exception as e:
                st.error(f"✗ Registration failed: {str(e)}")
    
    # Display registered voters
    st.subheader("Registered Voters")
    try:
        voters = voter_client.list()
        if voters.get("voters"):
            voter_df_data = []
            for v in voters["voters"]:
                voter_df_data.append({
                    "Voter ID": v.get('id'),
                    "Name": v.get('name'),
                    "Email": v.get('email')
                })
            
            import pandas as pd
            st.dataframe(pd.DataFrame(voter_df_data), use_container_width=True)
        else:
            st.info("No voters registered yet.")
    except Exception as e:
        st.error(f"Failed to fetch voters: {str(e)}")

def page_request_token():
    """Request blind tokens page (voter-only)"""
    st.title("🔑 Request Voting Token")
    
    # Voter-only access
    if not st.session_state.authenticated or st.session_state.user_type != "voter":
        st.warning("⚠️ Voter login required. Please log in as a voter first.")
        return
    
    st.write(f"**Voter:** {st.session_state.voter_name} (ID: {st.session_state.voter_id})")
    st.write("Request your blind voting token to participate in the election.")
    
    if st.button("Request Blind Token", use_container_width=True, type="primary"):
        try:
            # Get public key for blind signing
            pk_data = token_client.public_key()
            st.success("✓ Public key retrieved")
            
            # Issue token
            dummy_blinded = "blinded_msg_" + st.session_state.voter_id
            result = token_client.issue_token(st.session_state.voter_id, dummy_blinded)
            
            # Store token in session
            if "token" in result:
                st.session_state.voter_token = result.get("token")
            
            st.success(f"✓ Blind token issued successfully!")
            with st.expander("Token Details"):
                st.json(result)
        except Exception as e:
            st.error(f"✗ Failed to request token: {str(e)}")

def page_cast_vote():
    """Cast vote page (voter-only)"""
    st.title("🗳️ Cast Your Vote")
    
    # Voter-only access
    if not st.session_state.authenticated or st.session_state.user_type != "voter":
        st.warning("⚠️ Voter login required. Please log in as a voter first.")
        return
    
    st.write(f"**Voter:** {st.session_state.voter_name} (ID: {st.session_state.voter_id})")
    st.write("Cast your anonymous vote below.")
    
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    
    selected_candidate = st.selectbox("Select your candidate", candidates, key="candidate_select")
    
    if st.button("Cast Vote", use_container_width=True, type="primary"):
        try:
            # Get voter's token
            token_data = token_client.tokens_by_voter(st.session_state.voter_id)
            token = token_data[0].get("token", "") if isinstance(token_data, list) and token_data else ""
            
            if not token:
                st.error("✗ No valid token found. Please request a token first.")
            else:
                # Cast vote
                vote_data = {"candidate": selected_candidate}
                result = ballot_client.cast(st.session_state.voter_id, token, vote_data)
                st.success(f"✓ Vote cast successfully for {selected_candidate}!")
                with st.expander("Ballot Receipt"):
                    st.json(result)
        except Exception as e:
            st.error(f"✗ Failed to cast vote: {str(e)}")

def page_mixnet():
    """MixNet anonymization page (admin-only)"""
    st.title("🔀 MixNet Anonymization")
    
    # Admin-only access
    if not st.session_state.authenticated or st.session_state.user_type != "admin":
        st.warning("⚠️ Admin login required. Please log in as an admin first.")
        return
    
    st.write("**Admin Function:** Run the MixNet to anonymize and shuffle all ballots.")
    st.info("⚠️ This operation cannot be undone. Ensure all voting is complete before running.")
    
    layers = st.slider("Number of mixing layers", 1, 10, 3)
    
    if st.button("Run MixNet", use_container_width=True, type="primary"):
        try:
            result = admin_client.run_mixnet(layers=layers)
            st.success("✓ MixNet completed! Ballots anonymized and shuffled.")
            with st.expander("MixNet Result"):
                st.json(result)
        except Exception as e:
            st.error(f"✗ MixNet failed: {str(e)}")

def page_tally():
    """Tally results page (admin-only)"""
    st.title("📊 Election Results")
    
    # Admin-only access
    if not st.session_state.authenticated or st.session_state.user_type != "admin":
        st.warning("⚠️ Admin login required. Please log in as an admin first.")
        return
    
    st.write("**Admin View:** Complete election tallying and results.")
    
    try:
        ballots = ballot_client.list()
        if ballots.get("ballots"):
            tally = {}
            for b in ballots["ballots"]:
                candidate = b.get("candidate", "Unknown")
                tally[candidate] = tally.get(candidate, 0) + 1
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vote Count")
                for candidate, votes in sorted(tally.items(), key=lambda x: x[1], reverse=True):
                    st.metric(candidate, votes, delta=None)
            
            with col2:
                st.subheader("Percentages")
                total = sum(tally.values())
                for candidate, votes in sorted(tally.items(), key=lambda x: x[1], reverse=True):
                    percentage = (votes / total * 100) if total > 0 else 0
                    st.write(f"{candidate}: {percentage:.1f}%")
            
            # Export results
            st.subheader("Export Results")
            if st.button("Export as CSV"):
                import csv
                from io import StringIO
                
                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow(["Candidate", "Votes", "Percentage"])
                total = sum(tally.values())
                for candidate, votes in sorted(tally.items(), key=lambda x: x[1], reverse=True):
                    percentage = (votes / total * 100) if total > 0 else 0
                    writer.writerow([candidate, votes, f"{percentage:.1f}%"])
                
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name="election_results.csv",
                    mime="text/csv"
                )
        else:
            st.info("No ballots cast yet.")
    except Exception as e:
        st.error(f"Failed to fetch ballots: {str(e)}")

def page_logs():
    """System logs page (admin-only)"""
    st.title("📜 System Logs & Audit Trail")
    
    # Admin-only access
    if not st.session_state.authenticated or st.session_state.user_type != "admin":
        st.warning("⚠️ Admin login required. Please log in as an admin first.")
        return
    
    st.write("**Admin Function:** System audit trail and activity logs.")
    
    try:
        r = base_client.get("/logs/")
        logs = r.json()
        if logs:
            st.subheader("Recent Activity")
            log_entries = []
            for log in logs:
                log_type = log.get('log_type', 'INFO').upper()
                message = log.get('message', '')
                timestamp = log.get('created_at', 'N/A')
                log_entries.append({
                    "Timestamp": timestamp,
                    "Type": log_type,
                    "Message": message
                })
            
            import pandas as pd
            st.dataframe(pd.DataFrame(log_entries), use_container_width=True)
        else:
            st.info("No logs available.")
    except Exception as e:
        st.error(f"Failed to fetch logs: {str(e)}")

def page_logout():
    """Logout page"""
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.admin_token = None
    st.session_state.voter_id = None
    st.session_state.voter_name = None
    st.success("✓ Logged out successfully!")
    st.rerun()

# ===== SIDEBAR NAVIGATION =====

st.sidebar.title("🗳️ Secure Voting")

# Build navigation menu based on authentication state and user type
if not st.session_state.authenticated:
    # ===== PRE-LOGIN PAGES =====
    st.sidebar.markdown("### Pre-Login Menu")
    pages = {
        "🏠 Home": page_home,
        "📝 Register": page_register_voter,
        "🔐 System Access": page_admin_login,
    }
    menu_type = "Pre-Login"

elif st.session_state.user_type == "admin":
    # ===== ADMIN POST-LOGIN PAGES =====
    st.sidebar.markdown("### Admin Menu")
    pages = {
        "🏠 Home": page_home,
        "✍️ Register Voter": page_voter_registration,
        "🔑 Request Token": page_request_token,
        "🗳️ Cast Vote": page_cast_vote,
        "🔀 MixNet": page_mixnet,
        "📊 Tally": page_tally,
        "📜 Logs": page_logs,
        "🚪 Logout": page_logout,
    }
    menu_type = "Admin"

else:  # voter
    # ===== VOTER POST-LOGIN PAGES =====
    st.sidebar.markdown("### Voter Menu")
    pages = {
        "🏠 Home": page_home,
        "✍️ Register Voter": page_voter_registration,
        "🔑 Request Token": page_request_token,
        "🗳️ Cast Vote": page_cast_vote,
        "🚪 Logout": page_logout,
    }
    menu_type = "Voter"

# Navigation dropdown
selected_page = st.sidebar.selectbox("Navigate:", list(pages.keys()))

# Display authentication status in sidebar
st.sidebar.markdown("---")
if st.session_state.authenticated:
    if st.session_state.user_type == "admin":
        st.sidebar.success("✓ Admin Access")
        st.sidebar.caption("Full system control enabled")
    else:  # voter
        st.sidebar.success(f"✓ {st.session_state.voter_name}")
        st.sidebar.caption(f"Voter ID: {st.session_state.voter_id}")
else:
    st.sidebar.info("ℹ️ Not logged in")

st.sidebar.caption(f"Menu: {menu_type}")

# Execute selected page
pages[selected_page]()
