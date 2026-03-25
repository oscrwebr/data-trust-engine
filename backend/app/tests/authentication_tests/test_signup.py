from app.authentication.service import create_user
from app.workspaces.models import Notification
from app.workspaces.repository import add_workspace
from app.invites.repository import add_invite
from sqlalchemy import insert
from app.authentication.models import User
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

# Tests to ensure that an employee is added correctly when the create_user service is run
def test_create_user_service_adds_employee_correctly(db):
    image = create_test_image()

    dummy_user = {
        "name": "John Katherine Smith",
        "email": "jkatherinesmith@outlook.com",
        "preferred_username": "jkatherinesmith@outlook.com",
        "oid": "00000000-0000-0000-476j-987sdf88se", # This is random
    }

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh="ms-refresh-token".encode(), oid=oid, role="employee")
    admin_instance=db.execute(admin)

    workspace = add_workspace(db=db, name="Test Workspace", image=image)
    user = create_user(db=db, details=dummy_user, refresh="ms-refresh-token", ms_access_token="ms-access-token", role="employee", workspace_id=workspace.id)

    # assertions
    assert user # Check that there is a user object returned
    assert user.firstname == "John"
    assert user.surname == "Smith"
    assert user.email == dummy_user["email"]
    assert user.oid == dummy_user["oid"]
    assert user.role == "employee"
    

# Tests to ensure that an admin is added correctly when the create_user service is run
def test_create_user_service_adds_admin_correctly(db):
    image = create_test_image()
    dummy_user = {
        "name": "John Katherine Smith",
        "email": "jkatherinesmith@outlook.com",
        "preferred_username": "jkatherinesmith@outlook.com",
        "oid": "00000000-0000-0000-476j-987sdf88se", # This is random
    }

    user = create_user(db=db, details=dummy_user, refresh="ms-refresh-token", ms_access_token="ms-access-token", role="admin", workspace_id=None)

    # assertions
    assert user # Check that there is a user object returned
    assert user.firstname == "John"
    assert user.surname == "Smith"
    assert user.email == dummy_user["email"]
    assert user.oid == dummy_user["oid"]
    assert user.role == "admin"


# Test to ensure that sign up return 400 error when role is omitted
def test_signup_fails_without_role(client):
    req = client.build_request(
        method="get",
        url="/auth/sign-in/?next=/someUrl&signup=true"
    )
    response = client.send(request = req)
    
    assert response.status_code == 400

# Test to ensure that sign up return 400 error when role is not in the roles_dict
def test_signup_fails_with_bad_role(client):
    req = client.build_request(
        method="get",
        url="/auth/sign-in/?next=/someUrl&signup=true&role=100"
    )
    response = client.send(request = req)
    
    assert response.status_code == 400