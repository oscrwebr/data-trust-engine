from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .authentication.router import router as auth_router

from app.invites.router import router as invite_router
from app.scanning.router import router as scanning_router
from app.roles.router import router as roles_router

app = FastAPI()
app.include_router(invite_router)
app.include_router(scanning_router)
app.include_router(roles_router)

app.include_router(auth_router)

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

@app.get("/roles")
def roles():
    return {"status": "roles"}