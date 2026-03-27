from sqlalchemy import insert, select
import requests, json
from datetime import datetime, timezone
from sqlalchemy import func

from app.tests.ingestion_tests.ingestion_data import GRAPH_RESPONSE_ODATA_NEXT, GRAPH_RESPONSE_ODATA_LINK, GRAPH_RESPONSE_2_PERMISSIONS, GRAPH_RESPONSE_BATCH_25, GRAPH_RESPONSE_NOT_SHARED, GRAPH_RESPONSE_NO_FILE_OR_FOLDER, GRAPH_PERMISSIONS_NO_GRANTED_V2, GRAPH_RESPONSE_NO_ODATA_LINK
from app.authentication.models import User
from app.authentication.service import get_user_access
from app.ingestion import models
from app.ingestion.service import INIT_GRAPH_GET, GET_PERMISSIONS, GRAPH_BATCH_URL, DOWNLOAD_URL_GET, get_set_all_graph_files, get_download_link_by_graph_id, clean_folders_files_with_permissions
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

# Unit test to ensure that the function successfully pulls all one drive files and folders for a user
def test_files_and_folders_pulled_from_one_drive_correctly(db, requests_mock):
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
def test_files_pulled_without_next_link(db, requests_mock):
    ms_access_token = "fake-ms-access-token"
    # Create user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    # Mock the api response with only odata.deltaLink
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_ODATA_LINK,
        status_code=200
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

    # Ensure there is ONE API call to graph api with 'delta' in the path and the access token in the header
    assert len(mock_graph_init_get.request_history) == 1
    assert mock_graph_init_get.request_history[0].path.endswith("/delta") == True
    assert mock_graph_init_get.request_history[0]._request.headers["Authorization"] == f"Bearer {ms_access_token}"

    # Ensure that the single new file is successfully added to the database
    folder = db.execute(select_folders).all()
    assert len(folder) == 1

# Test to ensure that drive id is added for each file/folder
def test_drive_id_added_per_file(db, requests_mock):
    ms_access_token = "fake-ms-access-token"

    # create data for the two user that is being tested (adding permissions for both users)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

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

    # Mock for permissions
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

    # Ensure that the number of folders and files added match the number of folders and files with a drive_Id
    assert db.query(func.count(models.Folder.folder_id)).scalar() == db.query(func.count(models.Folder.drive_id)).scalar()
    assert db.query(func.count(models.IngestionFile.ingestion_file_id)).scalar() == db.query(func.count(models.IngestionFile.drive_id)).scalar()

# Test to ensure that the system can correctly batch requests for permissions in 20's
def test_ensure_permission_requests_batch_in_20(db, requests_mock):
    ms_access_token = "fake-ms-access-token"
    # Create user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    # Mock the api response with only over 20 shared files/folders
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_BATCH_25,
        status_code=200
    )
    # This will be used to ensure multiple requests are sent
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

    # Ensure that there are 2 calls to the 'mock_permissions_response'
    assert len(mock_permissions_response.request_history) == 2
    # Count the number of items in the first request body and ensure it is 20
    request_body = json.loads(mock_permissions_response.request_history[0]._request.body.decode('utf-8'))
    assert len(request_body["requests"]) == 20

# Test that the download url can be retrieved with the graph id
def test_download_link_retrieved_via_graph_id(db, requests_mock):
    # Creating the dummy user who's driveId the file will belong to
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), driveId="fake-drive-id", oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement)
    
    # Creating the dummy file that will be used
    insert_statement = insert(models.IngestionFile).values(graph_id="testgraphid1234", name="name_of_file", extension="docx", hash="dummy_hash", hash_type="sha256", last_modified=datetime.now(timezone.utc), web_url="dummy_url", parent_graph_id=None, drive_id="fake-drive-id")
    db.execute(insert_statement)

    # Mock the API call to graph
    download_url_get = requests_mock.get(
        url=DOWNLOAD_URL_GET.format(graph_id="testgraphid1234"),
        json={
            "@microsoft.graph.downloadUrl": "fake-download-url-returned-by-mock"
        },
        status_code=200
    )
    fake_msal = FakeMsal()
    download_url = get_download_link_by_graph_id(application=fake_msal, graph_id="testgraphid1234", db=db)

    # ASSERTIONS
    ## Ensure that a download link is returned
    assert download_url
    ## Ensure that the returned download link is the one returned by the mock api
    assert download_url == "fake-download-url-returned-by-mock"
    ## Ensure that there is a request to the mock api
    assert len(download_url_get.request_history) == 1
    ## Ensure that the download link was requested with an access token
    assert download_url_get.request_history[0]._request.headers["Authorization"] == f"Bearer {fake_msal.acquire_token_silent()["access_token"]}"

# Test that None returned if graph doesn't return 200 code when requesting download url
def test_none_if_400_returned_for_download_link_retrieval(db, requests_mock):
    # Creating the dummy user who's driveId the file will belong to
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), driveId="fake-drive-id", oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement)
    
    # Creating the dummy file that will be used
    insert_statement = insert(models.IngestionFile).values(graph_id="testgraphid1234", name="name_of_file", extension="docx", hash="dummy_hash", hash_type="sha256", last_modified=datetime.now(timezone.utc), web_url="dummy_url", parent_graph_id=None, drive_id="fake-drive-id")
    db.execute(insert_statement)

    # Mock the API call to graph
    download_url_get = requests_mock.get(
        url=DOWNLOAD_URL_GET.format(graph_id="testgraphid1234"),
        json={
            "@microsoft.graph.downloadUrl": "fake-download-url-returned-by-mock"
        },
        status_code=400
    )
    fake_msal = FakeMsal()
    download_url = get_download_link_by_graph_id(application=fake_msal, graph_id="testgraphid1234", db=db)

    # Assert nothing is returned
    assert download_url == None

# Test to ensure that when a drive has no shared files or folders, there is no redundant call to GRAPH API for permissions
def test_no_permissions_call_when_no_shared(db, requests_mock):
    ms_access_token = "fake-ms-access-token"
    # Create user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    # Mock the api response with item that has no file or folder attribute
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_NOT_SHARED,
        status_code=200
    )

    # handle permission requests
    mock_permissions_response = requests_mock.post(
        url=GRAPH_BATCH_URL,
        json=GRAPH_RESPONSE_2_PERMISSIONS
    )

    # Calling the function that handles graph ingestion
    output = get_set_all_graph_files(access_token=ms_access_token, id=user.user_id, db=db)
    assert output == {'repo_response_u_folders': {'status': 200}, 'repo_response_u_files': {'status': 200}} # Make sure that the lack of calls isn't because there was an error somewhere!

    # MAIN ASSERTION - ensure that there is no call for permissions - history of calls is empty
    assert mock_permissions_response.request_history == []


# Test to ensure that user_id_dict is utilised to reduce db calls when 'clean_folders_files_with_permissions()' function is used
def test_user_id_dict_used_instead_of_db_calls_for(db):
    # Create users required
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid_2 = "000001-4sdf44-55asdf7-6sdiy987"
    oid_3 = "000003-3ref343-74asd234-5ssdfy9345"
    oid_4 = "000004-45hkjhk45-324khkjh2-234ajkshfsd3"
    insert_first_user = insert(User).values({"firstname":"John", "surname":"Smith", "username":"johnSmith1@hotmail.com", "email":"JohnSmith1@hotmail.com", "refresh":encrypt_refresh("ms-refresh-token"), "oid":oid, "role":"employee"}).returning(User.user_id)
    insert_statement = insert(User).values([
        {"firstname":"Bruce", "surname":"Wayne", "username":"manbat@hotmail.com", "email":"manbat@hotmail.com", "refresh":encrypt_refresh("ms-refresh-token_2"), "oid":oid_2, "role":"admin"},
        {"firstname":"Peter", "surname":"Parker", "username":"spiderboy@hotmail.com", "email":"spiderboy@hotmail.com", "refresh":encrypt_refresh("ms-refresh-token_3"), "oid":oid_3, "role":"employee"},
        {"firstname":"Marty", "surname":"McFly", "username":"mcfly@hotmail.com", "email":"mcfly@hotmail.com", "refresh":encrypt_refresh("ms-refresh-token_4"), "oid":oid_4, "role":"admin"}
        ])
    user_id = db.execute(insert_first_user).scalar_one()
    db.execute(insert_statement)

    # Dummy data for function call
    folder_file_data = {
        'folder': [(1, '1H9872G9875T7K1!alkdsjhf878768asdf76876lasdkfj89876'), (2, '1H9872G9875T7K1!573'), (3, '1H9872G9875T7K1!575'), (4, '1H9872G9875T7K1!574')], 
        'file': [(1, '1H9872G9875T7K1!5784'), (2, '1H9872G9875T7K1!6326'), (3, '1H9872G9875T7K1!6466')]
        }
    permissions = {
        'folder': {
            '1H9872G9875T7K1!573': {'granted_permission': {'johnSmith1@hotmail.com', 'manbat@hotmail.com'}},
            '1H9872G9875T7K1!575': {'granted_permission': {'johnSmith1@hotmail.com', 'mcfly@hotmail.com'}},
            '1H9872G9875T7K1!574': {'granted_permission': {'mcfly@hotmail.com', 'manbat@hotmail.com'}}
        },
        'file': {
            '1H9872G9875T7K1!5784': {'granted_permission': {'johnSmith1@hotmail.com', 'manbat@hotmail.com'}},
            '1H9872G9875T7K1!6326': {'granted_permission': {'johnSmith1@hotmail.com', 'spiderboy@hotmail.com'}}
        }
    }

    # Calling function
    user_folders, user_files = clean_folders_files_with_permissions(folder_file_data=folder_file_data, permissions=permissions, id=user_id, db=db)
    assert len(user_folders) == 8
    assert len(user_files) == 5

# Test to ensure 400 status_code is returned if there is no deltaLink in the response from Graph API
def test_400_if_no_delta_link(db, requests_mock):
    ms_access_token = "fake-ms-access-token"
    # Create user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    # Mock the api response with no deltaLink
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_NO_ODATA_LINK,
        status_code=200
    )

    # Calling the function that handles graph ingestion
    output = get_set_all_graph_files(access_token=ms_access_token, id=user.user_id, db=db)

    # Ensure that there is a 400 error with a description of '@odata.deltaLink'
    assert output['status_code'] == 400
    assert output['error'] == "KeyError - '@odata.deltaLink'"

# Test to ensure 400 status_code is returned Graph API response is not 200
def test_400_if_not_200_response(db, requests_mock):
    ms_access_token = "fake-ms-access-token"
    # Create user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()

    # Mock the api response without success status (anything other than 200)
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_NO_ODATA_LINK,
        status_code=404
    )

    # Calling the function that handles graph ingestion
    output = get_set_all_graph_files(access_token=ms_access_token, id=user.user_id, db=db)

    # Ensure that there is a 400 error with a description of '@odata.deltaLink'
    assert output['status_code'] == 400
    assert output['error'] == "Couldn't retrieve!"

# Test to ensure when there is no user associated with the drive id retrieved from the ingestion file, api call should not be made and 'None' is returned
def test_no_request_if_no_user_for_file_drive_id(db, requests_mock):
    # Adding required data to the db
    insert_statement = insert(models.IngestionFile).values(graph_id="test_graph_id", name="test_name", extension="pdf", hash="dummy_hash", hash_type="sha1", last_modified=datetime.now(timezone.utc), web_url="fake_url", drive_id="drive_id_for_no_one")
    db.execute(insert_statement)
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement)

    # setting the mock api call
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_NO_ODATA_LINK,
        status_code=400
    )

    # Running the function for getting the download_link
    link = get_download_link_by_graph_id(application=FakeMsal(), graph_id="test_graph_id", db=db)

    # Assert None returned and no api call is made
    assert link == None
    assert mock_graph_init_get.request_history == []

# Test to ensure that no api call is made and nothing is returned if there is no ingestion file with the graph_id being requested
def test_no_request_if_graph_id_not_in_db(db, requests_mock):
    # setting the mock api call
    mock_graph_init_get = requests_mock.get(
        INIT_GRAPH_GET,
        json=GRAPH_RESPONSE_NO_ODATA_LINK,
        status_code=400
    )

    # Running the function for getting the download_link
    link = get_download_link_by_graph_id(application=FakeMsal(), graph_id="test_graph_id", db=db)

    # Assert None returned and no api call is made
    assert link == None
    assert mock_graph_init_get.request_history == []
