# Admin login page
# pages/00_login.py
import streamlit as st
from api_client import admin_client

st.title("🔐 Admin Login")

st.write("Log in with admin credentials to access admin features.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not username or not password:
        st.error("Please enter both username and password")
    else:
        try:
            result = admin_client.login(username, password)
            st.session_state.admin_token = result.get("access_token")
            st.session_state.admin_username = username
            st.success(f"Welcome, {username}!")
        except Exception as e:
            st.error(f"Login failed: {str(e)}")

# Show logout button if already logged in
if "admin_token" in st.session_state:
    st.success(f"✓ Logged in as {st.session_state.admin_username}")
    if st.button("Logout"):
        try:
            admin_client.revoke_current()
            del st.session_state.admin_token
            del st.session_state.admin_username
            st.success("Logged out successfully")
        except Exception as e:
            st.error(f"Logout error: {str(e)}")
