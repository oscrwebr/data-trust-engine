from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NotificationSchema(BaseModel):
   title: str
   body: str
   workspace_id: int

class RemoveSchema(BaseModel):
   notification_id: int