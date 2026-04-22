from app.scanning.models import Scan
from sqlalchemy.orm import Session
from app.roles.models import SensitivityCategory, SensitivitySubcategory
from app.ingestion.models import UserFiles
from app.authentication.models import User
from app.workspaces.models import user_workspace as UserWorkspace
from app.scanning.models import *
from app.invites.models import Invite
from app.roles.models import Role
from app.workspaces.models import pending_user_workspace as PendingUserWorkspace


def get_recent_scans(db: Session, workspace_id: int):
    return (
        db.query(Scan)
        .join(ScanFile, Scan.scan_id == ScanFile.scan_id)
        .join(IngestionFile, ScanFile.file_id == IngestionFile.ingestion_file_id)
        .join(UserFiles, IngestionFile.ingestion_file_id == UserFiles.file_id)
        .join(UserWorkspace, UserWorkspace.c.user_id == UserFiles.user_id)
        .filter(UserWorkspace.c.workspace_id == workspace_id)
        .order_by(Scan.started_at.desc())
        .distinct()
        .limit(10)
        .all()
    )

def get_recent_invites(db: Session, workspace_id: int):
    return (
        db.query(Invite)
        .filter(Invite.workspace_id == workspace_id)
        .order_by(Invite.created_at.desc())
        .limit(10)
        .all()
    )

def get_recent_role_changes(db: Session, workspace_id: int):
    return (
        db.query(Role)
        .filter(Role.workspace_id == workspace_id)
        .order_by(Role.last_updated.desc())
        .limit(10)
        .all()
    )

def get_all_workspace_files(db: Session, workspace_id: int):
    return (
        db.query(IngestionFile.ingestion_file_id)
        .join(UserFiles, IngestionFile.ingestion_file_id == UserFiles.file_id)
        .join(UserWorkspace, UserWorkspace.c.user_id == UserFiles.user_id)
        .filter(UserWorkspace.c.workspace_id == workspace_id)
        .distinct()
        .count()
        )

def get_all_pending_users(db: Session, workspace_id: int):
    return (
        db.query(PendingUserWorkspace.c.user_id)
        .filter(PendingUserWorkspace.c.workspace_id == workspace_id)
        .count()
    )

def get_all_workspace_employees(db: Session, workspace_id: int):
    return (
        db.query(User.user_id)
        .join(UserWorkspace, UserWorkspace.c.user_id == User.user_id)
        .filter(UserWorkspace.c.workspace_id == workspace_id)
        .distinct()
        .count()
    )