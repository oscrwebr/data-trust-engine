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

# Fake classes used for mocking
class FakeMsal():
    def get_accounts(self, *args, **kwargs):
        return ["This is the user account!"]
    def acquire_token_silent(self, *args, **kwargs):
        return {
            "access_token": "fake-ms-access-token",
            "refresh_token": "fake-ms-refresh-token"
        }


# Test that when the user hits the rename-file endpoint, if they are not an admin, they get a 401 error
def test_only_admin_has_access(db, client):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    refresh_family = create_refresh_family(db)

    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "employee"}, refresh_family_id=refresh_family.refresh_family_id)

    res = client.patch(
        url = "/ingestion/rename-file?graph_id=434E337FBAFF35FB!s6f07447f47f04e5884a1170d0179043b&new_name=Azure_fdev_test_tutorial",
        headers={"Authorization": f"Bearer {access}"}
    )
    
    # ASSERTIONS - ensure that unauthorised status code is returned (401)
    assert res.status_code == 401


# Test that when the user hits the rename-file endpoint, if all details are correct, the ingestion file that is being updated should have its name, weburl nad last modified date updated
def test_file_updated(db, client, requests_mock):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="admin", driveId="dummy-drive-id").returning(User)
    user = db.execute(insert_statement).scalar_one()

    refresh_family = create_refresh_family(db)

    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Dummy for ingestion File being tested
    file_insert_statement = insert(IngestionFile).values(
        graph_id="graph-1234",
        name="test-graph",
        extension="pdf",
        hash="dummy-hash",
        hash_type="sha256",
        last_modified=(datetime.now(timezone.utc) - timedelta(days=7)),
        web_url="original-web-url",
        drive_id="dummy-drive-id"
        ).returning(IngestionFile)
    file = db.execute(file_insert_statement).scalar_one()

    # Adding dependency override for application
    app.dependency_overrides[application] = lambda: FakeMsal()
    
    # Adding the mock for the requets to MSAL for the file update, returning 200
    date_val = datetime.now().replace(microsecond=0).isoformat()
    ms_return = requests_mock.patch(
        url=GRAPH_PATCH_NAME.format(graph_id="graph-1234"),
        json = {
            "name": "test-works.pdf",
            "webUrl": "dummy-return-url",
            "lastModifiedDateTime": date_val
        })

    res = client.patch(
        url = "/ingestion/rename-file?graph_id=graph-1234&new_name=test-works",
        headers={"Authorization": f"Bearer {access}"}
    )

    # ASSERTIONS
    assert res.status_code == 200
    # Ensure that the ingestion file has been updated accordingly
    get_ingestion_file = select(IngestionFile).where(IngestionFile.ingestion_file_id == file.ingestion_file_id)
    latest_file = db.execute(get_ingestion_file).scalar_one()
    assert latest_file.name == "test-works.pdf"
    assert latest_file.last_modified.isoformat() == date_val
    assert latest_file.web_url == "dummy-return-url"

# Test that the values in the patch request are as expected
def test_patch_request(db, client, requests_mock):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="admin", driveId="dummy-drive-id").returning(User)
    user = db.execute(insert_statement).scalar_one()

    refresh_family = create_refresh_family(db)

    access, refresh, _ = create_access_refresh(db, data={"userId": user.user_id, "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Dummy for ingestion File being tested
    file_insert_statement = insert(IngestionFile).values(
        graph_id="graph-1234",
        name="test-graph",
        extension="pdf",
        hash="dummy-hash",
        hash_type="sha256",
        last_modified=(datetime.now(timezone.utc) - timedelta(days=7)),
        web_url="original-web-url",
        drive_id="dummy-drive-id"
        ).returning(IngestionFile)
    file = db.execute(file_insert_statement).scalar_one()

    # Adding dependency override for application
    app.dependency_overrides[application] = lambda: FakeMsal()
    
    # Adding the mock for the requets to MSAL for the file update, returning 200
    date_val = datetime.now().replace(microsecond=0).isoformat()
    ms_return = requests_mock.patch(
        url=GRAPH_PATCH_NAME.format(graph_id="graph-1234"),
        json = {
            "name": "test-works.pdf",
            "webUrl": "dummy-return-url",
            "lastModifiedDateTime": date_val
        })

    res = client.patch(
        url = "/ingestion/rename-file?graph_id=graph-1234&new_name=test-works",
        headers={"Authorization": f"Bearer {access}"}
    )

    # ASSERTIONS
    assert res.status_code == 200
    assert len(ms_return.request_history) == 1
    assert ms_return.request_history[0]._request.url.split("/")[-1] == "graph-1234"
    assert ms_return.request_history[0]._request.headers["Authorization"] == "Bearer fake-ms-access-token"
    assert ms_return.request_history[0]._request.body.decode() == "{\"name\": \"test-works.pdf\"}"
