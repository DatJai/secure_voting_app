# Cast vote page
# pages/03_cast_vote.py
import streamlit as st
from api_client import ballot_client, voter_client, token_client

st.title("3️⃣ Cast Vote")

candidates = ["Candidate A", "Candidate B", "Candidate C"]

try:
    voters = voter_client.list()
    eligible_voters = [v["id"] for v in voters.get("voters", []) if v.get("has_token") and not v.get("has_voted")]

    selected_voter = st.selectbox("Select Voter", [""] + eligible_voters if eligible_voters else [""])
    selected_candidate = st.selectbox("Select Candidate", [""] + candidates)

    if st.button("Cast Vote"):
        if not selected_voter or not selected_candidate:
            st.error("Select both voter and candidate")
        else:
            # Get voter's token
            token_data = token_client.tokens_by_voter(selected_voter)
            
            # Cast vote via the ballot client
            vote_data = {"candidate": selected_candidate}
            if token_data and isinstance(token_data, list) and len(token_data) > 0:
                token = token_data[0].get("token", "")
            else:
                token = ""
            
            result = ballot_client.cast(selected_voter, token, vote_data)
            st.success(f"Vote cast successfully! Ballot ID: {result.get('id', 'N/A')}")
except Exception as e:
    st.error(f"Error: {str(e)}")
