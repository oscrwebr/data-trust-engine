from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class CreateWorkspace(BaseModel):
    name: Optional[str] = None
    image: Optional[bytes] = None