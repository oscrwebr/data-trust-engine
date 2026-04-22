from app.scanning.repository import get_user_workspace_id
from sqlalchemy.orm import Session
from app.dashboard import repository

def get_recent_activity(db: Session, user_id: int):
    workspace_id = get_user_workspace_id(db, user_id)

    if workspace_id is None:
        return None
    
    # Get all recent scans, invites and role changes
    scans = repository.get_recent_scans(db, workspace_id)
    invites = repository.get_recent_invites(db, workspace_id)
    role_changes = repository.get_recent_role_changes(db, workspace_id)

    recent_activity = []

    # Append to the recent activity list for sorting by most recent timestamp later on
    for scan in scans:
        recent_activity.append({
            "type": "scan_started",
            "scan_id": scan.scan_id,
            "timestamp": scan.started_at,
            "scan_type": scan.scan_type,
        })

        if scan.finished_at is not None:
            recent_activity.append({
                "type": "scan_completed",
                "scan_id": scan.scan_id,
                "timestamp": scan.finished_at,
                "scan_type": scan.scan_type,
            })

    for invite in invites:
        recent_activity.append({
            "type": "invite",
            "invite_id": invite.invite_id,
            "timestamp": invite.created_at,
            "email": invite.email,
        })

    for role_change in role_changes:
        recent_activity.append({
            "type": "role_change",
            "role_id": role_change.role_id,
            "role_name": role_change.name,
            "timestamp": role_change.last_updated,
        })

    # https://docs.python.org/3/howto/sorting.html - .sort()
    # Understanding lambda: https://stackoverflow.com/a/42966511
    recent_activity.sort(key=lambda x: x["timestamp"], reverse=True)
    return recent_activity[:5]
