from fastapi import APIRouter, HTTPException
from api.models.token import BlindedSignatureRequest, BlindedSignatureResponse, TokenRequest, TokenOut
from api.models.response import ResponseModel
from services.voting_authority import VotingAuthority
from db.connection import get_conn
from db.repositories.token_repository import TokenRepository

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.get("/public_key", response_model=dict)
def get_public_key():
	authority = VotingAuthority(get_conn())
	return authority.get_public_key()


@router.post("/issue", response_model=BlindedSignatureResponse)
def issue_blinded_signature(req: BlindedSignatureRequest):
	authority = VotingAuthority(get_conn())
	try:
		sig = authority.issue_blind_signature(req.blinded_hash, req.voter_id)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
	return BlindedSignatureResponse(blinded_signature=hex(sig))


@router.get("/by_voter/{voter_id}", response_model=TokenOut)
def get_token_by_voter(voter_id: str):
	repo = TokenRepository()
	try:
		token = repo.get_token_by_voter(voter_id)
		if not token:
			raise HTTPException(status_code=404, detail="token not found")
		return TokenOut(**token)
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
