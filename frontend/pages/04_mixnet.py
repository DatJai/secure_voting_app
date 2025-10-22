# Mixnet shuffle page
# pages/04_mixnet.py
import streamlit as st
from api_client import admin_client, ballot_client

st.title("4️⃣ MixNet Anonymization")

# Check if admin is logged in
if "admin_token" not in st.session_state:
    st.error("Admin login required. Please log in first.")
else:
    try:
        ballots = ballot_client.list()
        if not ballots.get("ballots"):
            st.info("No ballots to mix yet.")
        else:
            if st.button("Run MixNet"):
                result = admin_client.run_mixnet(layers=3)
                st.success("MixNet completed! Ballots anonymized.")
                st.json(result)
    except Exception as e:
        st.error(f"Error: {str(e)}")
