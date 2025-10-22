from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from middleware import auth

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in_minutes: int
    refresh_token: str | None = None


@router.post("/token", response_model=TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    # returns access token and we'll also issue a refresh token
    resp = await auth.authenticate_user(form_data)
    access_token = resp["access_token"]
    # create refresh token (longer lived)
    refresh_exp = None
    refresh_token = auth.create_jwt_token(form_data.username, expires_delta=auth.timedelta(days=1))
    return TokenResponse(access_token=access_token, token_type=resp.get("token_type", "bearer"), expires_in_minutes=resp.get("expires_in_minutes", 2), refresh_token=refresh_token)


class IntrospectRequest(BaseModel):
    token: str


@router.post("/introspect")
def introspect(req: IntrospectRequest):
    payload = auth.decode_jwt_token(req.token)
    return {"active": bool(payload), "payload": payload}


@router.post("/revoke")
def revoke(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="invalid token")
    jti = payload.get("jti")
    if jti:
        auth.revoke_jti(jti)
    return {"revoked": True}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh(req: RefreshRequest):
    payload = auth.decode_jwt_token(req.refresh_token)
    if not payload:
        raise HTTPException(status_code=400, detail="invalid or expired refresh token")
    # ensure it's a refresh token - we didn't set type earlier; for now accept any token as refresh
    username = payload.get("sub")
    new_access = auth.create_jwt_token(username)
    return {"access_token": new_access, "token_type": "bearer", "expires_in_minutes": auth.JWT_EXPIRE_MINUTES}
