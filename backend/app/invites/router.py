import secrets
import arrow

from app.invites import repository as invite_repository
from app.invites.models import Invite
from app.invites.service import set_pending_user_type_invite
from app.authentication import repository as user_repository
from app.authentication import service
from app.core.database import get_database
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from .service import create_invite, send_invite_service, check_invite
from .schema import InviteRequest
from fastapi.responses import RedirectResponse
from urllib.parse import quote
from app.workspaces.service import add_pending_user_to_workspace

from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token
from ..core.config import REDIRECT_URI, FRONTEND_BASE_URL

router = APIRouter(prefix="/invite", tags=["invite"])

@router.post("/send-invite")
async def send_invite(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], invite: InviteRequest):
    user = service.test_route(current_user.user_id, db=db)
    workspace = user.workspaces[0]
    time_now = datetime.now()
    result = await create_invite(db, invite, workspace, time_now, user.email)
    if(result == True):

        # Generate parameters
        token = str(secrets.token_hex(16))
        expiry = arrow.get(str(invite.expiry_date.date()), "YYYY-MM-DD")
        expiry = expiry.format("Do MMMM YYYY")

        

        # Record invite and new user in database (if user doesn't already exist)
        pending_user = user_repository.get_pending_user_by_email(db, invite.email)
        if not pending_user:
            pending_user = user_repository.add_user(db, invite.email, "invite")
            add_pending_user_to_workspace(db, workspace.id, pending_user.user_id)
        
        else:
            set_pending_user_type_invite(db, pending_user, "invite")
        
        invite_repository.add_invite(db, time_now, invite.expiry_date.date(), token, False, pending_user.user_id, workspace)
        await send_invite_service(db, invite.email, expiry, token, workspace, user)

    return {"success": result}

@router.get("/invite-processing")
async def process_invite(token: str = Query(...), db: Session = Depends(get_database)):
    
    invite = invite_repository.get_invite(db, token)

    # If no invite then redirect the user to you have already joined a workspace with this invite
    if not invite or invite.used == True:
        return RedirectResponse(f"{FRONTEND_BASE_URL}/workspace-joined")
    
    # Get the pending_user based on the invite
    pending_user = user_repository.get_pending_user_by_id(db, invite.user_id)

    # Check the invite
    result = check_invite(invite, db)

    workspace_id = invite.workspace_id
    # Check wether the invite expiry date
    if(result == "expired"):
        expiry = invite.expiry_date
        return RedirectResponse(f"{FRONTEND_BASE_URL}/invite-error/expired?date={expiry}&workspace={workspace_id}&pending_user_id={pending_user.user_id}")
    
    invite_repository.update_invite_used_value(db, invite.invite_id)
    next_url = "/dashboard?toast=signup"
    redirect_url = f"{REDIRECT_URI}/auth/sign-in?next={quote(next_url)}&signup=true&role=2&workspace_id={workspace_id}&token={token}"

    return RedirectResponse(redirect_url, status_code=302)

