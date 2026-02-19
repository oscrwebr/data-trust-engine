from fastapi import APIRouter
from .service import create_invite
from .schema import InviteRequest

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
async def send_invite(invite: InviteRequest):
    result = await create_invite(invite)
    return {"success": result}
