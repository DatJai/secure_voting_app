# Event logging utilities
# utils/logger.py
from db.repositories.log_repository import LogRepository

log_repo = LogRepository()

def add_log(message: str, log_type: str = "info"):
    log_repo.add_log(message, log_type)
