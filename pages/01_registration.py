# Voter registration page
# pages/01_registration.py
import streamlit as st
from db.repositories import VoterRepository
from utils.logger import add_log

def app():
    st.title("1️⃣ Registration")
    voter_repo = VoterRepository()

    st.subheader("Register New Voter")
    name = st.text_input("Voter Name")
    voter_id = st.text_input("Voter ID")

    if st.button("Register Voter"):
        if not name or not voter_id:
            st.error("Voter ID and Name are required")
        else:
            voter_repo.add_voter(voter_id, name)
            st.success(f"Voter '{name}' registered successfully")
            add_log(f"Voter registered: {voter_id} - {name}", "info")

    st.subheader("Registered Voters")
    voters = voter_repo.get_all_voters()
    if voters:
        for v in voters:
            st.write(f"{v['voter_id']} - {v['name']} | Token: {v['has_token']} | Voted: {v['has_voted']}")
    else:
        st.info("No voters registered yet.")
