from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    password: str
    scopes: Optional[str] = "admin"


class UserOut(BaseModel):
    username: str
    scopes: Optional[str]


class UserList(BaseModel):
    users: List[UserOut]
