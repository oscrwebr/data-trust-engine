import secrets
from app.invites import repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends
from .service import create_invite
from .schema import InviteRequest

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
def send_invite(invite: InviteRequest, db: Session=Depends(get_database)):
    result = create_invite(invite)
    if(result == True):

        # Record invite in database
        token = str(secrets.token_hex(16))
        repository.add_invite(db, datetime.now(), token, invite.expiry_date.date(), "sent", False)

    return {"success": result}
