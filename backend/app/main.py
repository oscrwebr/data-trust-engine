from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.invites.router import router as invite_router
from app.scanning.router import router as scanning_router
from app.roles.router import router as roles_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invite_router)
app.include_router(scanning_router)
app.include_router(roles_router)

@app.get("/dashboard")
def dashboard():
    return {"status": "dashboard"}