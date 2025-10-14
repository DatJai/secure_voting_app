# streamlit_app.py
import streamlit as st
from services.voting_authority import VotingAuthority
from services.voter_client import VoterClient
from services.mixnet import VerifiableMixNet
from db.repositories.voter_repository import VoterRepository
from db.repositories.ballot_repository import BallotRepository
from utils.logger import add_log
import secrets
from db.connection import get_conn

# -------------------
# Initialization
# -------------------
st.set_page_config(page_title="Secure Voting System", layout="wide")

if "authority" not in st.session_state:
    st.session_state.authority = VotingAuthority(get_conn())
if "voter_repo" not in st.session_state:
    st.session_state.voter_repo = VoterRepository()
if "ballot_repo" not in st.session_state:
    st.session_state.ballot_repo = BallotRepository()
if "mixnet" not in st.session_state:
    st.session_state.mixnet = VerifiableMixNet()
if "phase" not in st.session_state:
    st.session_state.phase = "registration"

authority = st.session_state.authority
voter_repo = st.session_state.voter_repo
ballot_repo = st.session_state.ballot_repo
mixnet = st.session_state.mixnet

# -------------------
# Sidebar navigation
# -------------------
pages = ["Registration", "Request Token", "Cast Vote", "Mix Network", "Tally Results", "Logs"]
page = st.sidebar.selectbox("Navigate", pages)

# -------------------
# Page: Registration
# -------------------
if page == "Registration":
    st.title("🛡️ Registration")
    st.write("Register voters in the system.")
    
    voter_name = st.text_input("Voter Name")
    voter_id = st.text_input("Voter ID")
    
    if st.button("Register Voter"):
        if voter_name and voter_id:
            voter_repo.add_voter(voter_id, voter_name)
            authority.register_voter(voter_id)
            add_log(f"Registered voter {voter_name} ({voter_id})", "info")
            st.success(f"Voter {voter_name} registered!")
        else:
            st.error("Please provide both Name and ID")
    
    st.subheader("Registered Voters")
    voters = voter_repo.get_all_voters()
    for v in voters:
        st.write(f"{v['voter_id']}: {v['name']} | Token: {v['has_token']} | Voted: {v['has_voted']}")

# -------------------
# Page: Request Token
# -------------------
elif page == "Request Token":
    st.title("🔑 Request Blind Token")
    voters = voter_repo.get_all_voters()
    voter_map = {v['voter_id']: v['name'] for v in voters if not v['has_token']}
    
    if voter_map:
        voter_id = st.selectbox("Select Voter", list(voter_map.keys()), format_func=lambda x: voter_map[x])
        if st.button("Request Token"):
            client = VoterClient(authority)
            token_hash, signature = client.create_blind_token(voter_id)
            voter_repo.update_token_status(voter_id, True)
            add_log(f"Token issued to {voter_map[voter_id]}", "success")
            st.success(f"Blind token issued for {voter_map[voter_id]}!")
    else:
        st.info("All voters have tokens or no voters registered.")

# -------------------
# Page: Cast Vote
# -------------------
elif page == "Cast Vote":
    st.title("🗳️ Cast Vote")
    voters = voter_repo.get_all_voters()
    eligible_voters = {v['voter_id']: v['name'] for v in voters if v['has_token'] and not v['has_voted']}
    
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    
    if eligible_voters:
        voter_id = st.selectbox("Select Voter", list(eligible_voters.keys()), format_func=lambda x: eligible_voters[x])
        candidate = st.selectbox("Select Candidate", candidates)
        
        if st.button("Cast Vote"):
            client = VoterClient(authority)
            # Retrieve token from DB
            token_data = client.token_repo.get_token_by_voter(voter_id)
            signature = int(token_data['signature'], 16)
            token_hash = token_data['token_hash']
            ballot_id = client.cast_vote(token_hash, signature, candidate)
            voter_repo.mark_voted(voter_id)
            add_log(f"Voter {eligible_voters[voter_id]} cast vote for {candidate}", "success")
            st.success(f"Vote cast successfully! Ballot ID: {ballot_id}")
    else:
        st.info("No eligible voters for casting vote.")

# -------------------
# Page: Mix Network
# -------------------
elif page == "Mix Network":
    st.title("🔀 Verifiable Mix Network")
    ballots = ballot_repo.get_all_ballots()
    
    if st.button("Run Mix Network"):
        mixed, proofs = mixnet.mix(ballots)
        st.session_state.mixed_ballots = mixed
        st.session_state.mix_proofs = proofs
        for p in proofs:
            add_log(f"Layer {p['layer']} shuffled {p['inputCount']} ballots", "info")
        st.success("Mix Network completed!")
    
    if "mixed_ballots" in st.session_state:
        st.subheader("Mixed Ballots")
        for b in st.session_state.mixed_ballots:
            st.write(f"{b['ballot_id']} → Encrypted: {b['encrypted']} | Candidate hidden")

# -------------------
# Page: Tally Results
# -------------------
elif page == "Tally Results":
    st.title("📊 Tally Results")
    if "mixed_ballots" in st.session_state:
        tally = {}
        for b in st.session_state.mixed_ballots:
            tally[b['candidate']] = tally.get(b['candidate'], 0) + 1
        st.subheader("Results")
        for c, v in tally.items():
            st.write(f"{c}: {v} votes")
    else:
        st.info("Run Mix Network first.")

# -------------------
# Page: Logs
# -------------------
elif page == "Logs":
    st.title("📜 System Logs")
    from db.repositories.log_repository import LogRepository
    log_repo = LogRepository()
    logs = log_repo.get_all_logs()
    
    for log in logs:
        st.write(f"[{log['created_at']}] ({log['log_type']}) {log['message']}")
