# frontend/api_client/__init__.py
from .base_client import BaseClient
from .admin_client import AdminClient
from .token_client import TokenClient
from .voter_client import VoterClient
from .ballot_client import BallotClient

base_client = BaseClient()
admin_client = AdminClient(base_client)
token_client = TokenClient(base_client)
voter_client = VoterClient(base_client)
ballot_client = BallotClient(base_client)
__all__ = ["base_client", "admin_client", "token_client", "voter_client", "ballot_client"]