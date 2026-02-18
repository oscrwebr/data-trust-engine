from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .service import create_invite

router = APIRouter(prefix="/invite", tags=["invite"])

class InviteRequest(BaseModel):
    email: str
    expiry_date: Optional[datetime] = None

@router.post("/send-invite")
async def send_invite(invite: InviteRequest):
    result = await create_invite(invite)
    print(result)
    return {"success":result}
