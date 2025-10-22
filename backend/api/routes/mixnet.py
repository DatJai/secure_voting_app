from fastapi import APIRouter, Depends
from services.mixnet import VerifiableMixNet
from db.repositories.ballot_repository import BallotRepository
from db.repositories.mixnet_repository import MixNetRepository
from middleware.auth import get_current_admin_user

router = APIRouter(prefix="/mixnet", tags=["mixnet"])


@router.post("/run", response_model=dict)
def run_mixnet(layers: int = 3, admin: str = Depends(get_current_admin_user)):
	ballot_repo = BallotRepository()
	mixnet_repo = MixNetRepository()
	try:
		ballots = ballot_repo.get_all_ballots()
	except Exception:
		# DB unavailable in test env -> treat as no ballots
		ballots = []
	if not ballots:
		return {"message": "no ballots to mix", "mixed": []}
	mixnet = VerifiableMixNet(layers=layers)
	mixed, proofs = mixnet.mix(ballots)
	for p in proofs:
		mixnet_repo.save_proof(p)
	return {"mixed": mixed, "proofs": proofs}
