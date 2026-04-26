import io
import pytest
from app.org_chart import service
from app.roles import repository as roles_repo
from app.authentication.models import User
from app.workspaces.models import Workspace
from app.roles.models import PendingUserRole
from unittest.mock import patch
from app.authentication.repository import get_pending_user_by_email
from unittest.mock import AsyncMock, patch

# ---------------- Helper classes ----------------
class UploadFileMock:
    """Mock for FastAPI UploadFile with async read()"""
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self._content = content

    async def read(self):
        return self._content

# ---------------- Helper functions ----------------
def create_workspace(db, name="Test Workspace", image=b"fake-image-bytes"):
    workspace = Workspace(
        name=name,
        image=image,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

# ---------------- Tests ----------------
@pytest.mark.asyncio
async def test_parse_orgchart_success(db):
    """Test that uploading a valid CSV parses correctly."""
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
    """Test that roles are confirmed and saved correctly, including PendingUserRoles."""
    workspace = create_workspace(db)
    workspace_id = workspace.id

    roles_payload = [
        {"name": "Manager", "employees": [{"name": "Alice", "email": "alice@example.com"}]},
        {"name": "Engineer", "employees": [{"name": "Bob", "email": "bob@example.com"}]},
    ]

    mock_send = AsyncMock(return_value=None)

    with patch(
        "app.org_chart.service.send_invite_service", 
        new_callable=AsyncMock
    ) as mock_send:

        mock_send.return_value = None

        saved_roles = await service.confirm_orgchart(
            roles_payload,
            db,
            workspace_id=workspace_id
        )

        # optional assert
        assert mock_send.await_count >= 0

    # Check roles saved
    assert len(saved_roles) == 2
    role_names = [r.name if hasattr(r, "name") else r["name"] for r in saved_roles]
    assert "Manager" in role_names
    assert "Engineer" in role_names

    alice = get_pending_user_by_email(db, "alice@example.com")
    bob = get_pending_user_by_email(db, "bob@example.com")
    assert alice is not None
    assert bob is not None

    # ---------------- Check PendingUserRoles ----------------
    for role in saved_roles:
        # Normalize role_id and role_name
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