from pydantic import BaseModel
from typing import Optional


class VoterCreate(BaseModel):
	name: str
	email: str


class VoterOut(BaseModel):
	voter_id: str
	name: str
	has_token: bool
	has_voted: bool


class VoterList(BaseModel):
	voters: list[VoterOut]
