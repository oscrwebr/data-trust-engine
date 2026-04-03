import os
from dotenv import load_dotenv

load_dotenv()

# Get the frontend host - will be different when different docker compose profiles are running
FRONTEND_HOST = os.environ.get("FRONTEND_HOST")

FRONTEND_BASE_URL = "http://{FRONTEND_HOST}:5173"
SCOPES = os.environ.get("SCOPES").split()