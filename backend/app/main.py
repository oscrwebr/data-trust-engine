from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.scanning.router import router as scanning_router
from app.roles.router import router as roles_router

app = FastAPI()
app.include_router(scanning_router)
app.include_router(roles_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def root():
    return {"status": "ok"}