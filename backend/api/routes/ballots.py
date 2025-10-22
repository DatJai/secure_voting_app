from fastapi import APIRouter, HTTPException
from api.models.ballot import BallotCreate, BallotOut
from api.models.response import ResponseModel
from services.voting_authority import VotingAuthority
from db.connection import get_conn
from db.repositories.ballot_repository import BallotRepository

router = APIRouter(prefix="/ballots", tags=["ballots"])


@router.post("/cast", response_model=ResponseModel)
def cast_ballot(b: BallotCreate):
	authority = VotingAuthority(get_conn())
	try:
		ballot_id = authority.verify_token_and_cast_ballot(b.token_hash, int(b.signature, 16), b.candidate)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return ResponseModel(message="ballot_cast", data={"ballot_id": ballot_id})


@router.get("/", response_model=list[BallotOut])
def list_ballots():
	repo = BallotRepository()
	try:
		ballots = repo.get_all_ballots()
	except Exception:
		ballots = []
	return [BallotOut(**b) for b in ballots]
