from sqlalchemy.orm import Session
from app.roles import service as roles_service
from app.authentication.repository import get_pending_user_by_email, add_user
from app.roles.models import PendingUserRole
from app.invites.service import send_invite_service
from app.invites.repository import add_invite
from app.workspaces.repository import get_workspace_by_workspace_id
from app.roles.models import Role
import secrets
import arrow
from datetime import datetime

async def parse_orgchart_file(file):
    import pandas as pd
    import io

    contents = await file.read()
    buffer = io.BytesIO(contents)

    if file.filename.endswith(".csv"):
        df = pd.read_csv(buffer)
    else:
        df = pd.read_excel(buffer, engine="openpyxl")

    roles = {}
    for _, row in df.iterrows():
        role = str(row["Role"]).strip()
        name = str(row["Name"]).strip()
        email = str(row["Email"]).strip()
        if role not in roles:
            roles[role] = []
        roles[role].append({"name": name, "email": email})

    formatted_roles = [{"name": r, "employees": e} for r, e in roles.items()]
    return {"roles": formatted_roles}


async def confirm_orgchart(roles: list, db: Session, workspace_id: int):
    saved_roles = []
    
    workspace = get_workspace_by_workspace_id(db, workspace_id)

    time_now = datetime.now()

    for r in roles:
        existing_role = db.query(Role).filter(
            Role.name == r["name"],
            Role.workspace_id == workspace_id
        ).first()

        if existing_role:
            role = existing_role
        else:
            role = roles_service.create_role(
                db,
                name=r["name"],
                thresholds=[],
                workspace_id=workspace_id,
                date=datetime.now()
            )
        saved_roles.append(role)

        role_id = role["role_id"] if isinstance(role, dict) else role.role_id

        for emp in r["employees"]:
            email = emp["email"]

            pending_user = get_pending_user_by_email(db, email)
            if not pending_user:
                pending_user = add_user(db, email, type="employee")

            existing = db.query(PendingUserRole).filter(
                PendingUserRole.user_id == pending_user.user_id,
                PendingUserRole.role_id == role_id
            ).first()

            if not existing:
                db.add(PendingUserRole(
                    user_id=pending_user.user_id,
                    role_id=role_id
                ))

            token = str(secrets.token_hex(16))

            expiry_date = datetime.now().date()  # or set default logic
            expiry_formatted = arrow.get(str(expiry_date), "YYYY-MM-DD").format("Do MMMM YYYY")

            await send_invite_service(
                db,
                email,
                expiry_formatted,
                token,
                workspace,
                None
            )

            add_invite(
                db,
                time_now,
                expiry_date,
                token,
                False,
                pending_user.user_id,
                workspace
            )

    db.commit()
    return saved_roles