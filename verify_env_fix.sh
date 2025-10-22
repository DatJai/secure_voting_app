#!/bin/bash

# Verify .env Loading Fix
# This script checks if all environment variables are properly loaded

set -e

echo "════════════════════════════════════════════════════════════════"
echo "       ✅ Environment Variables Loading - Verification"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check 1: Verify .env.backend exists
echo "1️⃣  Checking if .env.backend exists..."
if [ -f "/workspace/backend/.env.backend" ]; then
    echo "   ✅ .env.backend found"
else
    echo "   ❌ .env.backend NOT found"
    exit 1
fi
echo ""

# Check 2: Verify DATABASE_URL is in .env.backend
echo "2️⃣  Checking DATABASE_URL in .env.backend..."
if grep -q "DATABASE_URL" /workspace/backend/.env.backend; then
    echo "   ✅ DATABASE_URL found in .env.backend"
    echo "   Value: $(grep DATABASE_URL /workspace/backend/.env.backend | head -1)"
else
    echo "   ❌ DATABASE_URL NOT found in .env.backend"
    exit 1
fi
echo ""

# Check 3: Test environment loading
echo "3️⃣  Testing environment loading in Python..."
cd /workspace/backend

python3 << 'PYEOF'
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env.backend"
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DATABASE_URL")
admin_user = os.getenv("ADMIN_USERNAME")

if db_url:
    print("   ✅ DATABASE_URL loaded successfully")
    print(f"      Value: {db_url}")
else:
    print("   ❌ DATABASE_URL NOT loaded")
    exit(1)

if admin_user:
    print("   ✅ ADMIN_USERNAME loaded successfully")
    print(f"      Value: {admin_user}")
else:
    print("   ⚠️  ADMIN_USERNAME not loaded")
PYEOF

echo ""

# Check 4: Check if PostgreSQL is running
echo "4️⃣  Checking PostgreSQL installation..."
if command -v psql &> /dev/null; then
    echo "   ✅ psql found"
    PSQL_VERSION=$(psql --version)
    echo "   Version: $PSQL_VERSION"
else
    echo "   ⚠️  psql not found (PostgreSQL may not be installed)"
fi
echo ""

# Check 5: Check Python imports
echo "5️⃣  Checking Python dependencies..."
python3 << 'PYEOF'
try:
    import psycopg2
    print("   ✅ psycopg2 installed")
except ImportError:
    print("   ❌ psycopg2 NOT installed")
    exit(1)

try:
    from dotenv import load_dotenv
    print("   ✅ python-dotenv installed")
except ImportError:
    print("   ❌ python-dotenv NOT installed")
    exit(1)

try:
    from fastapi import FastAPI
    print("   ✅ FastAPI installed")
except ImportError:
    print("   ❌ FastAPI NOT installed")
    exit(1)
PYEOF

echo ""

# Check 6: Verify backend files updated
echo "6️⃣  Verifying backend files are updated..."
if grep -q "env_path = Path" /workspace/backend/db/connection.py; then
    echo "   ✅ db/connection.py updated with env loading"
else
    echo "   ❌ db/connection.py NOT updated"
    exit 1
fi

if grep -q "env_path = Path" /workspace/backend/main.py; then
    echo "   ✅ main.py updated with env loading"
else
    echo "   ❌ main.py NOT updated"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "   ✅ ALL CHECKS PASSED!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo "   1. Start PostgreSQL: sudo systemctl start postgresql"
echo "   2. Start backend: cd /workspace/backend && python main.py"
echo "   3. Test in Streamlit: Open http://localhost:8501"
echo ""
