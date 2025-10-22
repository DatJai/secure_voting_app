#!/bin/bash
# Start backend API

cd /workspace/backend

# Set PYTHONPATH so imports work correctly
export PYTHONPATH=/workspace/backend

# Run uvicorn
uvicorn main:app --reload --port 8000 --host 127.0.0.1
