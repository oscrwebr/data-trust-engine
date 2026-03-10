import secrets
import arrow

from app.invites import repository as invite_repository
from app.authentication import repository as user_repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from .service import create_invite, send_invite_service, check_invite
from .schema import InviteRequest
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
async def send_invite(invite: InviteRequest, db: Session=Depends(get_database)):
    result = await create_invite(invite)
    if(result == True):

        # Generate parameters
        token = str(secrets.token_hex(16))
        expiry = arrow.get(str(invite.expiry_date.date()), "YYYY-MM-DD")
        expiry = expiry.format("Do MMMM YYYY")

        #Send invite
        await send_invite_service(invite.email, expiry, token)

        # Record invite and new user in database (if user doesn't already exist)
        user = user_repository.get_by_email(db, invite.email)
        if not user:
            user = user_repository.add_user(db, invite.email)
        
        invite_repository.add_invite(db, datetime.now(), invite.expiry_date.date(), "sent", False, user.user_id, token)
        
    return {"success": result}

@router.get("/invite-processing")
async def process_invite(token: str = Query(...), db: Session = Depends(get_database)):
    
    invite = invite_repository.get_invite(db, token)

    # Check the expiry date
    result = check_invite(invite, db)

    if(result == "used"):
        return RedirectResponse(f"http://localhost:5173/invite-error/used")

    if(result == "expired"):
        return RedirectResponse(f"http://localhost:5173/invite-error/expired?date={invite.expiry_date}")
    
    return RedirectResponse("http://localhost:8000/auth/sign-in?next=/", status_code=302)

