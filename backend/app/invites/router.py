import secrets
from app.invites import repository as invite_repository
from app.authentication import repository as user_repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends
from .service import create_invite
from .schema import InviteRequest

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
async def send_invite(invite: InviteRequest, db: Session=Depends(get_database)):
    result = await create_invite(invite)
    if(result == True):

        # Record invite and new user in database
        user = user_repository.add_user(db, invite.email)
        invite_repository.add_invite(db, datetime.now(), invite.expiry_date.date(), "sent", False, user.id)
        
    return {"success": result}
