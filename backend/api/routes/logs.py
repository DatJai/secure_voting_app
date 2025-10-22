from fastapi import APIRouter, Depends
from db.repositories.log_repository import LogRepository
from middleware.auth import get_current_admin_user

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", response_model=dict)
def add_log(message: str, log_type: str = "info", admin: str = Depends(get_current_admin_user)):
	repo = LogRepository()
	repo.add_log(message, log_type)
	return {"message": "log added"}


@router.get("/", response_model=list)
def get_logs():
	repo = LogRepository()
	try:
		return repo.get_all_logs()
	except Exception:
		# fallback: return empty list
		return []
