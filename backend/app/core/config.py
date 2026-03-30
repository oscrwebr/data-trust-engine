import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_BASE_URL = "http://localhost:5173"
SCOPES = os.environ.get("SCOPES").split()