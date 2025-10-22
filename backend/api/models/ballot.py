from pydantic import BaseModel


class BallotCreate(BaseModel):
	token_hash: str
	signature: str
	candidate: str


class BallotOut(BaseModel):
	ballot_id: str
	candidate: str
	token_hash: str


class BallotList(BaseModel):
	ballots: list[BallotOut]

