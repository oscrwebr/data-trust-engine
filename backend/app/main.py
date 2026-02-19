from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from invites.router import router as invite_router
from app.scanning.router import router as scanning_router

app = FastAPI()
app.include_router(invite_router, scanning_router)

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