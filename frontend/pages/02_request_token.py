# Request voting token page
# pages/02_request_token.py
import streamlit as st
from api_client import token_client, voter_client

st.title("2️⃣ Request Blind Token")

try:
    voters = voter_client.list()
    voter_options = [v["id"] for v in voters.get("voters", []) if not v.get("has_token")]

    selected_voter = st.selectbox("Select Voter", [""] + voter_options if voter_options else [""])

    if st.button("Request Blind Token"):
        if not selected_voter:
            st.error("Please select a voter")
        else:
            # Get public key
            pk_data = token_client.public_key()
            st.info("Blind token issuance initiated (public key received)")
            
            # In a real scenario, you would blind the message locally here
            # For now, we simulate with a dummy blinded message
            dummy_blinded = "dummy_blinded_message"
            
            result = token_client.issue_token(selected_voter, dummy_blinded)
            st.success(f"Blind token issued for voter {selected_voter}")
except Exception as e:
    st.error(f"Error: {str(e)}")
