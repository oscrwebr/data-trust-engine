from fastapi import APIRouter
from typing import Annotated
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/invite", tags=["invite"])

class InviteRequest(BaseModel):
    email: str
    expiry_date: Optional[datetime] = None

@router.post("/send-invite")
async def send_invite(invite: InviteRequest):
    print(invite.email)
    print(invite.expiry_date)
    return {"success":True}
