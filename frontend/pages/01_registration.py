# Voter registration page
# pages/01_registration.py
import streamlit as st
from api_client import voter_client

st.title("1️⃣ Registration")

st.subheader("Register New Voter")
name = st.text_input("Voter Name")
email = st.text_input("Voter Email")

if st.button("Register Voter"):
    if not name or not email:
        st.error("Voter Name and Email are required")
    else:
        try:
            result = voter_client.register(name, email)
            st.success(f"Voter '{name}' registered successfully")
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")

st.subheader("Registered Voters")
try:
    voters = voter_client.list()
    if voters.get("voters"):
        for v in voters["voters"]:
            st.write(f"{v.get('id', 'N/A')} - {v.get('name', 'N/A')} | Email: {v.get('email', 'N/A')}")
    else:
        st.info("No voters registered yet.")
except Exception as e:
    st.error(f"Could not fetch voters: {str(e)}")
