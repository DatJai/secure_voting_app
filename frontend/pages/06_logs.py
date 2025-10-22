# Logs page
# pages/06_logs.py
import streamlit as st
from api_client import base_client

st.title("6️⃣ System Logs")

try:
    r = base_client.get("/logs/")
    logs = r.json()
    if logs.get("logs"):
        for log in logs["logs"]:
            st.write(f"[{log.get('created_at', 'N/A')}] {log.get('log_type', 'INFO').upper()} - {log.get('message', '')}")
    else:
        st.info("No logs yet.")
except Exception as e:
    st.error(f"Error: {str(e)}")
