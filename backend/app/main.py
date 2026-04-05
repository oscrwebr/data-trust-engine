from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .authentication.router import router as auth_router
from starlette.middleware.sessions import SessionMiddleware

from app.invites.router import router as invite_router
from app.scanning.router import router as scanning_router
from app.roles.router import router as roles_router
from app.workspaces.router import router as workspaces_router
from app.org_chart.router import router as org_chart_router
from app.ingestion.router import router as ingestion_router
from app.file_dashboard.router import router as files_dashboard_router

app = FastAPI()
app.include_router(invite_router)
app.include_router(scanning_router)
app.include_router(roles_router)
app.include_router(workspaces_router)
app.include_router(auth_router)
app.include_router(org_chart_router)
app.include_router(ingestion_router)
app.include_router(files_dashboard_router)

app.add_middleware(SessionMiddleware, secret_key="data-trust-engine-21a")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard")
def dashboard():
    return {"status": "dashboard"}