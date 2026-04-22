from sqlalchemy import insert, select
import requests, json
from datetime import datetime, timezone, timedelta
from sqlalchemy import func

from app.main import app
from app.core.security import application
from app.authentication.models import User
from app.authentication.service import create_access_refresh
from app.authentication.repository import create_refresh_family
from app.ingestion.models import IngestionFile
from app.ingestion.service import GRAPH_PATCH_NAME
from app.core.security import encrypt_refresh, decrypt_refresh
from app.workspaces.models import Workspace
from app.workspaces.repository import add_user_workspace

from app.tests.workspace_tests.test_workspace import create_test_image

# Fake classes used for mocking
class FakeMsal():
    def get_accounts(self, *args, **kwargs):
        return ["This is the user account!"]
    def acquire_token_silent(self, *args, **kwargs):
        return {
            "access_token": "fake-ms-access-token",
            "refresh_token": "fake-ms-refresh-token"
        }

# Test that when the user hits the delete-file endpoint, if they are not an admin, they get a 401 error
def test_only_admin_has_access(db, client):
    ms_access_token = "fake-ms-access-token"

    # create data for the user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    refresh_family = create_refresh_family(db)

    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "employee"}, refresh_family_id=refresh_family.refresh_family_id)

    res = client.delete(
        url = "/ingestion/delete-file?graph_id=graph-1234",
        headers={"Authorization": f"Bearer {access}"}
    )
    
    # ASSERTIONS - ensure that unauthorised status code is returned (401)
    assert res.status_code == 401

# Test that if the admin and file owner are not in the same workspace, 400 error is returned
def test_admin_file_owner_same_workspace(db, client):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="admin", driveId="dummy-drive-id-admin").returning(User)
    user = db.execute(insert_statement).scalar_one()

    oid = "000000-7sdf77-88asdf8-234sldfkj"
    insert_statement = insert(User).values(firstname="Mark", surname="Grayson", username="invincible@hotmail.com", email="Invincible@hotmail.com", refresh=encrypt_refresh("ms-refresh-token-2"), oid=oid, role="employee", driveId="dummy-drive-id-to-be-deleted").returning(User)
    user_2 = db.execute(insert_statement).scalar_one()

    # Creating tokens for admin
    refresh_family = create_refresh_family(db)
    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Creating the workspace for the admin, but not the user
    image = create_test_image()
    workspace_insert = insert(Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    # Adding admin to his workspace
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], user.user_id)

    # Creating the dummy ingestion file
    file_insert_statement = insert(IngestionFile).values(
        graph_id="graph-1234",
        name="test-graph",
        extension="pdf",
        hash="dummy-hash",
        hash_type="sha256",
        last_modified=(datetime.now(timezone.utc) - timedelta(days=7)),
        web_url="original-web-url",
        drive_id="dummy-drive-id-to-be-deleted"
        ).returning(IngestionFile)
    file = db.execute(file_insert_statement).scalar_one()

    # Making the call to the endpoint, expecting 400 error
    res = client.delete(
        url = "/ingestion/delete-file?graph_id=graph-1234",
        headers={"Authorization": f"Bearer {access}"}
    )

    # ASSERTIONS
    assert res.status_code == 400

# Test that if the file doesn't exist, 400 error is returned
def test_400_if_file_does_not_exist(db, client):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="admin").returning(User)
    user = db.execute(insert_statement).scalar_one()

    oid = "000000-7sdf77-88asdf8-234sldfkj"
    insert_statement = insert(User).values(firstname="Mark", surname="Grayson", username="invincible@hotmail.com", email="Invincible@hotmail.com", refresh=encrypt_refresh("ms-refresh-token-2"), oid=oid, role="employee").returning(User)
    user_2 = db.execute(insert_statement).scalar_one()

    # Creating tokens for admin
    refresh_family = create_refresh_family(db)
    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Creating the workspace for the admin, but not the user
    image = create_test_image()
    workspace_insert = insert(Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    # Adding admin to his workspace
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], user.user_id)

    # Making the call to the endpoint, expecting 400 error
    res = client.delete(
        url = "/ingestion/delete-file?graph_id=graph-1234",
        headers={"Authorization": f"Bearer {access}"}
    )

    # ASSERTIONS
    assert res.status_code == 400

# Test that when microsoft returns 204, user is returned a 200 status
def test_200_when_ms_return_204(db, client, requests_mock):
    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="admin").returning(User)
    user = db.execute(insert_statement).scalar_one()

    oid = "000000-7sdf77-88asdf8-234sldfkj"
    insert_statement = insert(User).values(firstname="Mark", surname="Grayson", username="invincible@hotmail.com", email="Invincible@hotmail.com", refresh=encrypt_refresh("ms-refresh-token-2"), oid=oid, role="employee", driveId="dummy-drive-id-to-be-deleted").returning(User)
    user_2 = db.execute(insert_statement).scalar_one()

    # Creating tokens for admin
    refresh_family = create_refresh_family(db)
    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Creating the workspace for the admin, but not the user
    image = create_test_image()
    workspace_insert = insert(Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    # Adding admin and employee to the workspace
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], user.user_id)
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], user_2.user_id)

    # Creating the dummy ingestion file
    file_insert_statement = insert(IngestionFile).values(
        graph_id="graph-1234",
        name="test-graph",
        extension="pdf",
        hash="dummy-hash",
        hash_type="sha256",
        last_modified=(datetime.now(timezone.utc) - timedelta(days=7)),
        web_url="original-web-url",
        drive_id="dummy-drive-id-to-be-deleted"
        ).returning(IngestionFile)
    file = db.execute(file_insert_statement).scalar_one()

    # Adding dependency override for application
    app.dependency_overrides[application] = lambda: FakeMsal()

    # Mock request
    delete_ms_response = requests_mock.delete(
        url=GRAPH_PATCH_NAME.format(graph_id="graph-1234"),
        status_code=204
    )

    # Making the call to the endpoint, expecting 204
    res = client.delete(
        url = "/ingestion/delete-file?graph_id=graph-1234",
        headers={"Authorization": f"Bearer {access}"}
    )

    # ASSERTIONS
    assert res.status_code == 200
    assert delete_ms_response.request_history[0]._request.url.split("/")[-1] == 'graph-1234'
    assert delete_ms_response.request_history[0]._request.headers["Authorization"] == "Bearer fake-ms-access-token"
    print(delete_ms_response.request_history[0]._request.headers.__dict__)
