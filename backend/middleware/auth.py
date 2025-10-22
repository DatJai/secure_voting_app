from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
import os
from datetime import datetime, timedelta
import jwt
from db.repositories.user_repository import UserRepository
from db.repositories.revoked_token_repository import RevokedTokenRepository
import bcrypt
import uuid

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "2"))  # default 2 minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Demo user database
_user_repo = UserRepository()
_revoked_repo = RevokedTokenRepository()

# in-memory revoked jti fallback when DB not available
_REVOKED_SET: set[str] = set()

# Fallback in-memory user store used when DB is unavailable (tests / dev)
_FALLBACK_USERS = {
    os.getenv("ADMIN_USERNAME", "admin"): {
        "username": os.getenv("ADMIN_USERNAME", "admin"),
        "password_hash": bcrypt.hashpw(os.getenv("ADMIN_PASSWORD", "adminpass").encode(), bcrypt.gensalt()).decode(),
        "scopes": "admin",
    }
}


def create_jwt_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    jti = str(uuid.uuid4())
    # pull scopes from DB (fallback to in-memory)
    try:
        user = _user_repo.get_user(username) or {}
    except Exception:
        user = _FALLBACK_USERS.get(username, {})
    scopes = user.get("scopes", "").split(",") if user else []
    payload = {"sub": username, "exp": expire, "scopes": scopes, "jti": jti}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT returns str in modern versions
    return token


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # check revocation
        jti = payload.get("jti")
        if jti:
            try:
                if _revoked_repo.is_revoked(jti):
                    return None
            except Exception:
                # fallback to in-memory set
                if jti in _REVOKED_SET:
                    return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


def revoke_jti(jti: str):
    try:
        _revoked_repo.revoke_token(jti)
    except Exception:
        _REVOKED_SET.add(jti)


async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = _user_repo.get_user(form_data.username)
    except Exception:
        # fallback to in-memory user
        user = _FALLBACK_USERS.get(form_data.username)
    # If DB returned None (no user), also check fallback in-memory
    if not user:
        user = _FALLBACK_USERS.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # verify password
    hashed = user.get("password_hash")
    if not hashed or not bcrypt.checkpw(form_data.password.encode(), hashed.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_jwt_token(user["username"]) 
    return {"access_token": token, "token_type": "bearer", "expires_in_minutes": JWT_EXPIRE_MINUTES}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


async def get_current_admin_user(username: str = Depends(get_current_user)):
    try:
        user = _user_repo.get_user(username)
    except Exception:
        user = _FALLBACK_USERS.get(username)
    # If DB returned None, fallback to in-memory
    if not user:
        user = _FALLBACK_USERS.get(username)
    scopes = []
    if user:
        scopes = user.get("scopes", "").split(",")
    if not user or "admin" not in scopes:
        raise HTTPException(status_code=403, detail="User is not an admin")
    return username
