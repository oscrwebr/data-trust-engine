from sqlalchemy import insert, select
import requests

from app.tests.ingestion_tests.ingestion_data import GRAPH_RESPONSE_ODATA_NEXT, GRAPH_RESPONSE_ODATA_LINK, GRAPH_RESPONSE_2_PERMISSIONS
from app.authentication.models import User
from app.authentication.service import get_user_access
from app.ingestion import models
from app.ingestion.service import INIT_GRAPH_GET, GET_PERMISSIONS, GRAPH_BATCH_URL, DOWNLOAD_URL_GET, get_set_all_graph_files
from app.core.security import encrypt_refresh, decrypt_refresh

# Unit test to ensure that the function successfully pulls all one drive files and folders for a user
def test_files_and_folders_pulled_from_one_drive_correctly(client, db, requests_mock):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    oid_2 = "000001-4sdf44-55asdf7-6sdiy987"
    insert_statement_2 = insert(User).values(firstname="Bruce", surname="Wayne", username="manbat@hotmail.com", email="manbat@hotmail.com", refresh=encrypt_refresh("ms-refresh-token_2"), oid=oid_2, role="admin").returning(User)
    user_2 = db.execute(insert_statement_2).scalar_one()

    # Ensure that both user 1 has no deltalink in the DB

    # Mocking API calls
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_ODATA_NEXT,
        status_code=200
    )
    
    mock_graph_odata_next_get = requests_mock.get(
        url="https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id%2cname%2clastModifiedDateTime%2cparentReference%2cfile%2cfolder%2cwebUrl%2ccontent.downloadUrl%2cshared&token=some_token",
        json = GRAPH_RESPONSE_ODATA_LINK,
        status_code=200
    )
    # This is what is returned when the function for getting permissions of shared files makes a batch post request
    mock_permissions_response = requests_mock.post(
        url=GRAPH_BATCH_URL,
        json=GRAPH_RESPONSE_2_PERMISSIONS
    )

    # Ensure that ingestion files and folders are empty
    select_files = select(models.IngestionFile)
    select_folders = select(models.Folder)
    file = db.execute(select_files).all()
    folder = db.execute(select_folders).all()
    assert file == [] # Making sure that ingestion_file is empty to begin with
    assert folder == [] # Making sure that folder is empty to begin with

    # Calling the function that handles graph ingestion
    output = get_set_all_graph_files(access_token=ms_access_token, id=user.user_id, db=db)

    # ASSERTIONS
    # Make sure that the number of folders added is correct (5)
    file = db.execute(select_files).all()
    assert len(file) == 2
    # Make sure that the number of files added is correct (2)
    folder = db.execute(select_folders).all()
    assert len(folder) == 4
    # Ensure there is ONE API call to graph api with 'delta' in the path and the access token in the header
    assert len(mock_graph_init_get.request_history) == 1
    assert mock_graph_init_get.request_history[0].path.endswith("/delta") == True
    assert mock_graph_init_get.request_history[0]._request.headers["Authorization"] == f"Bearer {ms_access_token}"

    # Ensure there is ONE API call for 'odata.nextLink', with the access token in the header.
    assert len(mock_graph_odata_next_get.request_history) == 1
    assert mock_graph_odata_next_get.request_history[0]._request.headers["Authorization"] == f"Bearer {ms_access_token}"

    # Ensure there is ONE POST request for permissions, as there is less than 20 files that need their permissions found
    # Also make sure there is an access token in the header
    assert len(mock_permissions_response.request_history) == 1
    assert mock_permissions_response.request_history[0]._request.headers["Authorization"] == f"Bearer {ms_access_token}"

    # Ensure that a delta link is updated for the user whose files have been retrieved
    user_select = select(User).where(User.user_id == user.user_id)
    user_1 = db.execute(user_select).scalar_one()
    assert user_1.deltaLink == "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id%2cname%2clastModifiedDateTime%2cparentReference%2cfile%2cfolder%2cwebUrl%2ccontent.downloadUrl%2cshared&token=token"

    # Ensure that files were added to the user_files table (length should be files + 1)
    user_files_select = select(models.UserFiles)
    user_files = db.execute(user_files_select).all()
    assert len(user_files) == 3

    # Ensure that files were added to the user_folders table (length should be folders + 1)
    user_folders_select = select(models.UserFolders)
    user_folders = db.execute(user_folders_select).all()
    assert len(user_folders) == 5

# Test ensuring system can pull files without an '@odata.nextLink'

# Test to ensure that the system can correctly batch requests for permissions in 20's