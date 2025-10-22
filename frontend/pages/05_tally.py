# Tally votes page
# pages/05_tally.py
import streamlit as st
from api_client import ballot_client

st.title("5️⃣ Tally Results")

try:
    ballots = ballot_client.list()
    if not ballots.get("ballots"):
        st.info("No ballots to tally.")
    else:
        tally = {}
        for b in ballots["ballots"]:
            candidate = b.get("candidate", "Unknown")
            tally[candidate] = tally.get(candidate, 0) + 1

        st.subheader("Election Results")
        for candidate, votes in sorted(tally.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{candidate}: {votes} votes")
except Exception as e:
    st.error(f"Error: {str(e)}")
