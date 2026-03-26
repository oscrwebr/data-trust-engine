# app/orgChart/service.py
from sqlalchemy.orm import Session
from app.roles import service as roles_service
from app.authentication.repository import get_pending_user_by_email, add_user
from app.roles.models import PendingUserRole

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


def confirm_orgchart(roles: list, db: Session):
    saved_roles = []

    for r in roles:
        role = roles_service.create_role(
            db,
            name=r["name"],
            thresholds=[],
            workspace_id=1
        )
        saved_roles.append(role)

        role_id = role["role_id"] if isinstance(role, dict) else role.role_id

        for emp in r["employees"]:
            email = emp["email"]

            pending_user = get_pending_user_by_email(db, email)

            if not pending_user:
                pending_user = add_user(db, email)

            existing = db.query(PendingUserRole).filter(
                PendingUserRole.user_id == pending_user.user_id,
                PendingUserRole.role_id == role_id
            ).first()

            if not existing:
                db.add(PendingUserRole(
                    user_id=pending_user.user_id,
                    role_id=role_id
                ))

    db.commit()
    return saved_roles