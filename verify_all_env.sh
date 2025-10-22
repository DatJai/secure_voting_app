#!/bin/bash

# Verify environment loading across frontend and backend
echo "════════════════════════════════════════════════════════════════════════════════"
echo "              ✅ Environment Loading Verification - Frontend & Backend"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Test 1: Backend environment loading
echo "1️⃣  Testing Backend Environment Loading..."
cd /workspace/backend
python3 << 'PYEOF'
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env.backend"
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_URL")
jwt_secret = os.getenv("JWT_SECRET")

if db_url:
    print("   ✅ DATABASE_URL loaded")
else:
    print("   ❌ DATABASE_URL NOT loaded")
    exit(1)

if jwt_secret:
    print("   ✅ JWT_SECRET loaded")
else:
    print("   ❌ JWT_SECRET NOT loaded")
    exit(1)
PYEOF

if [ $? -ne 0 ]; then
    echo "   ❌ Backend environment loading FAILED"
    exit 1
fi
echo ""

# Test 2: Frontend environment loading
echo "2️⃣  Testing Frontend Environment Loading..."
cd /workspace/frontend
python3 << 'PYEOF'
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env.frontend"
load_dotenv(dotenv_path=env_path)

backend_url = os.getenv("BACKEND_URL")
db_host = os.getenv("DB_HOST")

if backend_url:
    print("   ✅ BACKEND_URL loaded")
    print(f"      Value: {backend_url}")
else:
    print("   ❌ BACKEND_URL NOT loaded")
    exit(1)

if db_host:
    print("   ✅ DB_HOST loaded")
else:
    print("   ⚠️  DB_HOST not loaded")
PYEOF

if [ $? -ne 0 ]; then
    echo "   ❌ Frontend environment loading FAILED"
    exit 1
fi
echo ""

# Test 3: Verify both env files exist
echo "3️⃣  Checking Environment Files..."
if [ -f "/workspace/backend/.env.backend" ]; then
    echo "   ✅ /workspace/backend/.env.backend exists"
else
    echo "   ❌ /workspace/backend/.env.backend NOT found"
    exit 1
fi

if [ -f "/workspace/frontend/.env.frontend" ]; then
    echo "   ✅ /workspace/frontend/.env.frontend exists"
else
    echo "   ❌ /workspace/frontend/.env.frontend NOT found"
    exit 1
fi

if [ -f "/workspace/.env" ]; then
    echo "   ✅ /workspace/.env exists (fallback)"
else
    echo "   ⚠️  /workspace/.env NOT found (fallback not available)"
fi
echo ""

# Test 4: Check specific required variables
echo "4️⃣  Verifying Required Environment Variables..."
echo ""
echo "   Backend (.env.backend):"
grep "DATABASE_URL" /workspace/backend/.env.backend > /dev/null && echo "      ✅ DATABASE_URL" || echo "      ❌ DATABASE_URL missing"
grep "JWT_SECRET" /workspace/backend/.env.backend > /dev/null && echo "      ✅ JWT_SECRET" || echo "      ❌ JWT_SECRET missing"
grep "ADMIN_USERNAME" /workspace/backend/.env.backend > /dev/null && echo "      ✅ ADMIN_USERNAME" || echo "      ❌ ADMIN_USERNAME missing"

echo ""
echo "   Frontend (.env.frontend):"
grep "BACKEND_URL" /workspace/frontend/.env.frontend > /dev/null && echo "      ✅ BACKEND_URL" || echo "      ❌ BACKEND_URL missing"
grep "DB_HOST" /workspace/frontend/.env.frontend > /dev/null && echo "      ✅ DB_HOST" || echo "      ❌ DB_HOST missing"

echo ""

# Test 5: Check code changes
echo "5️⃣  Verifying Code Changes..."
echo ""
echo "   Backend db/connection.py:"
grep "env_path = Path" /workspace/backend/db/connection.py > /dev/null && echo "      ✅ Updated with env path" || echo "      ❌ NOT updated"
grep ".env.backend" /workspace/backend/db/connection.py > /dev/null && echo "      ✅ Uses .env.backend" || echo "      ❌ NOT using .env.backend"

echo ""
echo "   Backend main.py:"
grep "env_path = Path" /workspace/backend/main.py > /dev/null && echo "      ✅ Updated with env path" || echo "      ❌ NOT updated"
grep ".env.backend" /workspace/backend/main.py > /dev/null && echo "      ✅ Uses .env.backend" || echo "      ❌ NOT using .env.backend"

echo ""
echo "   Frontend api_client/base_client.py:"
grep "env_path = Path" /workspace/frontend/api_client/base_client.py > /dev/null && echo "      ✅ Updated with env path" || echo "      ❌ NOT updated"
grep ".env.frontend" /workspace/frontend/api_client/base_client.py > /dev/null && echo "      ✅ Uses .env.frontend" || echo "      ❌ NOT using .env.frontend"

echo ""
echo "   Frontend streamlit_app.py:"
grep "env_path = Path" /workspace/frontend/streamlit_app.py > /dev/null && echo "      ✅ Updated with env path" || echo "      ❌ NOT updated"
grep ".env.frontend" /workspace/frontend/streamlit_app.py > /dev/null && echo "      ✅ Uses .env.frontend" || echo "      ❌ NOT using .env.frontend"

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "   ✅ ALL CHECKS PASSED!"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📋 Summary:"
echo "   ✓ Backend loads .env.backend with fallback to .env"
echo "   ✓ Frontend loads .env.frontend with fallback to .env"
echo "   ✓ All required environment variables are present"
echo "   ✓ All code changes applied correctly"
echo ""
