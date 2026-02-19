from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.scanning.router import router as scanning_router

app = FastAPI()
app.include_router(scanning_router)

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