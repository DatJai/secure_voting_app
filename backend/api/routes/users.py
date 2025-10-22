from fastapi import APIRouter, HTTPException, Depends
import re
import bcrypt
from db.repositories.user_repository import UserRepository
from middleware.auth import get_current_admin_user
from api.models.user import UserCreate as UserCreateModel, UserOut, UserList

router = APIRouter(prefix="/users", tags=["users"])
user_repo = UserRepository()

# small blacklist for breached/common passwords (extend as needed)
_COMMON_PASSWORDS = {"password", "12345678", "qwerty123", "adminpass", "password123"}


def _validate_username(username: str) -> bool:
    return bool(re.fullmatch(r"^[A-Za-z0-9_]{3,32}$", username))


def _validate_password(pw: str) -> bool:
    # min 8 chars, at least one lower, one upper, one digit, one special char
    if len(pw) < 8:
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"\d", pw):
        return False
    if not re.search(r"[^A-Za-z0-9]", pw):
        return False
    if pw.lower() in _COMMON_PASSWORDS:
        return False
    return True


@router.post("/register", dependencies=[Depends(get_current_admin_user)])
def register_user(u: UserCreateModel):
    if not _validate_username(u.username):
        raise HTTPException(status_code=422, detail="username must be 3-32 chars and contain only letters, numbers, and underscores")
    if not _validate_password(u.password):
        raise HTTPException(status_code=422, detail="password must be at least 8 chars and include upper, lower, digit and a special character and not be a common password")

    try:
        existing = user_repo.get_user(u.username)
    except Exception:
        existing = None
    if existing:
        raise HTTPException(status_code=409, detail="user already exists")

    hashed = bcrypt.hashpw(u.password.encode(), bcrypt.gensalt()).decode()
    try:
        user_repo.create_user(u.username, hashed, scopes=u.scopes or "admin")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "user created", "username": u.username}


@router.get("/", response_model=UserList, dependencies=[Depends(get_current_admin_user)])
def list_users():
    try:
        conn_users = user_repo.get_user  # to ensure method exists
        # fetch all users directly (repo lacks list_all; do a simple query)
        from db.connection import get_conn
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT username, scopes FROM users ORDER BY username")
            rows = cur.fetchall()
        conn.close()
        users = [UserOut(username=r["username"], scopes=r.get("scopes")) for r in rows]
    except Exception:
        # fallback: return the fallback in-memory users
        from middleware.auth import _FALLBACK_USERS
        users = [UserOut(username=k, scopes=v.get("scopes")) for k, v in _FALLBACK_USERS.items()]
    return UserList(users=users)
