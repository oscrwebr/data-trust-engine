import secrets
import arrow

from app.invites import repository as invite_repository
from app.authentication import repository as user_repository
from app.authentication import service
from app.workspaces.repository import get_workspace_by_user_id
from app.core.database import get_database
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from .service import create_invite, send_invite_service, check_invite
from .schema import InviteRequest
from fastapi.responses import RedirectResponse
from urllib.parse import quote

from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
async def send_invite(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], invite: InviteRequest):
    user = service.test_route(current_user.user_id, db=db)
    workspace = get_workspace_by_user_id(db, current_user.user_id)
    time_now = datetime.now()
    result = await create_invite(db, invite, workspace, time_now, user.email)
    if(result == True):

        # Generate parameters
        token = str(secrets.token_hex(16))
        expiry = arrow.get(str(invite.expiry_date.date()), "YYYY-MM-DD")
        expiry = expiry.format("Do MMMM YYYY")

        #Send invite
        await send_invite_service(db, invite.email, "2023-03-03", token, workspace, user)

        # Record invite and new user in database (if user doesn't already exist)
        user = user_repository.get_pending_user_by_email(db, invite.email)
        if not user:
            user = user_repository.add_user(db, invite.email)
        
        invite_repository.add_invite(db, time_now, "2023-03-03", token, False, user.user_id, workspace)

    return {"success": result}

@router.get("/invite-processing")
async def process_invite(token: str = Query(...), db: Session = Depends(get_database)):
    
    invite = invite_repository.get_invite(db, token)

    # If no invite then redirect the user to you have already joined a workspace with this invite
    if not invite or invite.used == True:
        return RedirectResponse(f"http://localhost:5173/workspace-joined")
    
    # Get the pending_user based on the invite
    user = user_repository.get_pending_user_by_id(db, invite.user_id)

    # Check the invite
    result = check_invite(invite, db)

    # Check wether the invite expiry date
    if(result == "expired"):
        expiry = invite.expiry_date
        workspace_id = invite.workspace_id
        return RedirectResponse(f"http://localhost:5173/invite-error/expired?date={expiry}&workspace={workspace_id}")
    
    next_url = "/?toast=signup"
    redirect_url = f"http://localhost:8000/auth/sign-in?next={quote(next_url)}&signup=true&role=2"

    return RedirectResponse(redirect_url, status_code=302)

