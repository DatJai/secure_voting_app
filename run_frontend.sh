#!/bin/bash
# Start Streamlit frontend

cd /workspace/frontend

# Optional: Set BACKEND_URL if not already set
export BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

# Run Streamlit
streamlit run streamlit_app.py
