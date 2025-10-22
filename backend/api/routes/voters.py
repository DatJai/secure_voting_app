from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.models.voter import VoterCreate, VoterOut
from api.models.response import ResponseModel
from db.repositories.voter_repository import VoterRepository
from services.voting_authority import VotingAuthority
from db.connection import get_conn

router = APIRouter(prefix="/voters", tags=["voters"])


@router.post("/register", response_model=ResponseModel)
def register_voter(v: VoterCreate):
	repo = VoterRepository()
	try:
		# Auto-generate voter ID (VOTER-001, VOTER-002, etc.)
		last_voter = repo.get_last_voter()
		if last_voter:
			# Extract number from last voter ID
			last_id = last_voter.get("voter_id", "VOTER-000")
			try:
				last_num = int(last_id.split("-")[1])
			except (IndexError, ValueError):
				last_num = 0
		else:
			last_num = 0
		
		new_voter_id = f"VOTER-{last_num + 1:03d}"
		repo.add_voter(new_voter_id, v.name, v.email)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

	# Register in authority as well (best-effort)
	try:
		authority = VotingAuthority(get_conn())
		authority.register_voter(new_voter_id)
	except Exception:
		pass

	return ResponseModel(message="voter registered", data={"id": new_voter_id, "name": v.name})


@router.get("/", response_model=List[VoterOut])
def list_voters():
	repo = VoterRepository()
	try:
		voters = repo.get_all_voters()
		# voters come from RealDictCursor; ensure booleans are python bools
		return [VoterOut(**v) for v in voters]
	except Exception:
		# fallback: return empty list when DB unavailable
		return []
