from fastapi import FastAPI
from api.routes import voters, tokens, ballots, mixnet, logs, auth, users
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables early
env_path = Path(__file__).parent / ".env.backend"
load_dotenv(dotenv_path=env_path)

# Fallback to .env if .env.backend not found
if not os.getenv("DATABASE_URL"):
	load_dotenv()


def create_app() -> FastAPI:
	app = FastAPI(title="Secure Voting Authority API")
	app.include_router(voters.router)
	app.include_router(tokens.router)
	app.include_router(ballots.router)
	app.include_router(mixnet.router)
	app.include_router(logs.router)
	app.include_router(auth.router)
	app.include_router(users.router)
	return app


app = create_app()


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
