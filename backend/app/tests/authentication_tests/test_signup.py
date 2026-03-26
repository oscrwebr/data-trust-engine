from app.main import app
from fastapi import APIRouter, Request
from sqlalchemy import insert, select
from PIL import Image
from io import BytesIO
from datetime import datetime
import secrets
import requests
import pytest

from app.authentication.service import create_user, DRIVE_DATA_GRAPH_URL
from app.workspaces.models import Notification
from app.workspaces.repository import add_workspace
from app.invites.repository import add_invite
from app.authentication.models import User
from app.authentication.router import get_session
from app.core.security import application, decrypt_refresh
from app.core.database import get_database

# Mocking the MSAL dependency
class FakeMsal():
    def acquire_token_by_auth_code_flow(self, *args, **kwargs): # We don't care about what is actually passed in - just that this is returned!
        return {
            "id_token_claims": {
                "oid": "000000-7sdf77-88asdf8-9sdiy99",
                "name": "John Katherine Smith",
                "email": "jkatherinesmith@outlook.com",
                "preferred_username": "jkatherinesmith@outlook.com"
            },
            "refresh_token": "refresh_from_dummy_MSAL_class",
            "access_token": "access_from_dummy_MSAL_class"
        }
# Mocking the get_session function that's used for dependency injection
class FakeRequests():
    def __init__(self):
        self.session = {}


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

# Integration test that ensures a user's refresh token and driveId are added when they sign up'
def test_drive_id_and_refresh_added_for_user(client, db, requests_mock):
    # Setting up FakeRequests class for dependency injection override
    fake_requests = FakeRequests()
    fake_requests.session["flow"] = "flow"
    fake_requests.session["next"] = "/test"
    fake_requests.session["signup"] = True
    fake_requests.session["role"] = 1
    fake_requests.session["workspace_id"] = 1

    # overriding dependencies used by the router for '/success/'
    app.dependency_overrides[application] = lambda: FakeMsal()
    app.dependency_overrides[get_database] = lambda: db
    app.dependency_overrides[get_session] = lambda: fake_requests

    # Setting the URL interception for getting the driveId
    mock_get = requests_mock.get(
        DRIVE_DATA_GRAPH_URL,
        json={
            "id": "test_drive_id"
        },
        status_code=200
        )
    
    # Ensuring that there is no user in the user table
    select_statement = select(User)
    users = db.execute(select_statement).all()
    assert users == []

    # GET request for the '/success/' router
    client.get("/auth/success/")

    # Selecting the user from the db and ensuring that all the details required to be added are there
    users = db.execute(select_statement).all()[0][0]
    assert users.firstname == "John"
    assert users.surname == "Smith"
    assert users.email == "jkatherinesmith@outlook.com"
    assert users.username == "jkatherinesmith@outlook.com"
    assert users.oid == "000000-7sdf77-88asdf8-9sdiy99"
    assert decrypt_refresh(users.refresh) == "refresh_from_dummy_MSAL_class"
    assert users.driveId == "test_drive_id"

    # ensure that the request for driveId was made with the access token
    assert mock_get.request_history[0]._request.headers.get("Authorization") == "Bearer access_from_dummy_MSAL_class"