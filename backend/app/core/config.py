import os
from dotenv import load_dotenv

load_dotenv()

# Get the frontend host - will be different when different docker compose profiles are running
FRONTEND_BASE_URL = os.environ.get("FRONTEND_HOST")
SCOPES = os.environ.get("SCOPES").split()
REDIRECT_URI = os.environ.get("REDIRECT_URI")