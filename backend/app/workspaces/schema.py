from fastapi import FastAPI
from pydantic import BaseModel
from app.authentication.models import User
from typing import Optional

app = FastAPI()

class NotificationSchema(BaseModel):
   title: str
   body: str
   workspace_id: int

class MessageSchema(BaseModel):
   employees: list[int]
   body: Optional[str]

class RemoveSchema(BaseModel):
   notification_id: int