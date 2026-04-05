from app.authentication.service import create_user
from app.workspaces.models import Notification
from app.workspaces.repository import add_workspace, add_user_workspace
from app.invites.repository import add_invite
from sqlalchemy import insert
from app.authentication.models import User
from app.authentication.repository import add_user
from PIL import Image
from io import BytesIO
from datetime import datetime
import secrets

# Creating test image 
def create_test_image():
    img = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.getvalue()

# Test to ensure that a notification gets created when an employee has accepted an invite
def test_create_user_service_to_add_employee_creates_notification(db):
    image = create_test_image()
    token = str(secrets.token_hex(16))
    dummy_user = {
        "name": "John Katherine Smith",
        "email": "jkatherinesmith@outlook.com",
        "preferred_username": "jkatherinesmith@outlook.com",
        "oid": "00000000-0000-0000-476j-987sdf88se", # This is random
    }

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    admin_instance=db.execute(admin)

    pending_user = add_user(db, "SandraGhost1@hotmail.com", "invite")

    workspace = add_workspace(db=db, name="Test Workspace", image=image)
    add_user_workspace(db, workspace.id, admin_instance.inserted_primary_key[0])
    add_invite(db=db, createdAt=datetime.now(), expiryDate="2030-03-03", token=token, used=False, user_id=pending_user.user_id, workspace=workspace)
    create_user(db=db, details=dummy_user, refresh="ms-refresh", ms_access_token="ms-access-token", role="employee", workspace_id=workspace.id)

    # assertions
    assert db.query(Notification).count() == 1