import io
import pytest
from app.org_chart import service
from app.roles import repository as roles_repo
from app.authentication.models import User
from app.workspaces.models import Workspace
from app.roles.models import PendingUserRole
from unittest.mock import patch
from app.invites.service import send_invite_service
from app.authentication.repository import get_pending_user_by_email

class UploadFileMock:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self._content = content

    async def read(self):
        return self._content

def create_workspace(db, name="Test Workspace", image=b"fake-image-bytes"):
    workspace = Workspace(
        name=name,
        image=image,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

@pytest.mark.asyncio
async def test_parse_orgchart_success(db):
    csv_content = b"Role,Name,Email\nManager,Alice,alice@example.com\nEngineer,Bob,bob@example.com"
    file = UploadFileMock("orgchart.csv", csv_content)

    result = await service.parse_orgchart_file(file)

    assert "roles" in result
    roles = result["roles"]
    role_names = [r["name"] for r in roles]
    assert "Manager" in role_names
    assert "Engineer" in role_names
    assert any(emp["email"] == "alice@example.com" for r in roles for emp in r["employees"])

@pytest.mark.asyncio
async def test_confirm_orgchart_success(db):
    workspace = create_workspace(db)
    workspace_id = workspace.id

    roles_payload = [
        {"name": "Manager", "employees": [{"name": "Alice", "email": "alice@example.com"}]},
        {"name": "Engineer", "employees": [{"name": "Bob", "email": "bob@example.com"}]},
    ]

    async def fake_send_invite(*args, **kwargs):
        return None

    with patch.object(send_invite_service, "__call__", side_effect=fake_send_invite):
        saved_roles = await service.confirm_orgchart(roles_payload, db, workspace_id=workspace_id)

    assert len(saved_roles) == 2
    role_names = [r.name if hasattr(r, "name") else r["name"] for r in saved_roles]
    assert "Manager" in role_names
    assert "Engineer" in role_names

    alice = get_pending_user_by_email(db, "alice@example.com")
    bob = get_pending_user_by_email(db, "bob@example.com")
    assert alice is not None
    assert bob is not None

    for role in saved_roles:
        role_id = role.role_id if hasattr(role, "role_id") else role["role_id"]
        role_name = role.name if hasattr(role, "name") else role["name"]

        if role_name == "Manager":
            assigned_user = alice
        elif role_name == "Engineer":
            assigned_user = bob
        else:
            continue

        user_role = db.query(PendingUserRole).filter(
            PendingUserRole.user_id == assigned_user.user_id,
            PendingUserRole.role_id == role_id
        ).first()
        assert user_role is not None, f"{assigned_user.email} should have role {role_name} assigned"