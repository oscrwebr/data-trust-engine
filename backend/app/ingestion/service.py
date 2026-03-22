from msal import ConfidentialClientApplication
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from collections import defaultdict

from ..core.security import decrypt_refresh, encrypt_refresh
from ..core.config import SCOPES
from . import repository
from ..authentication import service as auth_service


INIT_GRAPH_GET = "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id,name,lastModifiedDateTime,parentReference,file,folder,webUrl,content.downloadUrl,shared"
DOWNLOAD_URL_GET = "https://graph.microsoft.com/v1.0/me/drive/items/{graph_id}?select=content.downloadUrl"
GET_PERMISSIONS = "me/drive/items/{graph_id}/permissions"
GRAHP_BATCH_URL = "https://graph.microsoft.com/v1.0/$batch"


def get_user_access(application: ConfidentialClientApplication, user_id, db:Session) -> str | None:
    # This is to get the access token for users - THAT ARE ALREADY LOGGED IN!
    user_details = auth_service.check_get_by_id(user_id, db)
    access_token = None
    
    if user_details:
        account = application.get_accounts(username=user_details.username)
        if account:
            tokens = application.acquire_token_silent(scopes=SCOPES, account=account[0])
            access_token = tokens["access_token"]
            # Rotate the refresh token in the DB
            enc_refresh = encrypt_refresh(tokens["refresh_token"])
            auth_service.rotate_ms_refresh(user_id, enc_refresh, db)

        else:
            account = application.acquire_token_by_refresh_token(refresh_token=decrypt_refresh(user_details.refresh), scopes=SCOPES)
            access_token = account["access_token"]
            # Rotate the refresh token in the DB
            enc_refresh = encrypt_refresh(account["refresh_token"])
            auth_service.rotate_ms_refresh(user_id, enc_refresh, db)
    else:
        return None

    return access_token

def get_values_data(folders: dict, files: dict, shared_folder_files: dict, values: list[dict]):
    '''
    Function that will take in three dictionaries containing retrieved data for both folders and files, and a dictionary of shared folders and files. It will also take in a list of dictionaries returned by the json response from Graph API.
    It will then return two dictionaries 'folders' and 'files' and a list of dictionaries 'shared_folder_files'.
    - 'folders' - Entries will consist of a key made from the graph_id and value that is an instance of the Folder class from the related schema
    - 'files' - Entries will consist of a key made from the graph_id and value that is an instance of the File class from the related schema
    - 'shared_folder_files' - Entries will consist of a 'graph_id' and 'type' that will specify what file should be used in the permissions batch query and later what database table should be updated (user-file or user-folder)
    '''

    for item in values:
        if "folder" in item: # This means that the item is a folder
            # This is in case the folder is the root folder itself
            if "id" in item["parentReference"]:
                parent_id = item["parentReference"]["id"]
            else:
                parent_id = None # This is the root directory!
            
            id = item["id"]

            # Checking if the folder is shared
            if "shared" in item:
                shared_folder_files[id] = "folder"

            folders[id] = {
                "graph_id": id,
                "name": item["name"],
                "web_url": item["webUrl"],
                "parent_graph_id":parent_id
            }
        elif "file" in item:
            id = item["id"]
            item_name = item["name"]
            # setting the hash type - using desired order
            if "sha256Hash" in (hashes := item["file"]["hashes"]):
                item_hash = ("sha256Hash", hashes["sha256Hash"])
            elif "quickXorHash" in hashes:
                item_hash = ("quickXorHash", hashes["quickXorHash"])
            elif "sha1Hash" in hashes:
                item_hash = ("sha1Hash", hashes["sha1Hash"])
            else:
                item_hash = (None, None)

            # Checking if the file is shared
            if "shared" in item:
                shared_folder_files[id] = "file"

            files[id] = {
                "graph_id": id,
                "name": item_name,
                "extension": item_name.split(".")[-1],
                "hash_type": item_hash[0],
                "hash": item_hash[1],
                "last_modified": datetime.fromisoformat(item["lastModifiedDateTime"]),
                "web_url": item["webUrl"],
                "parent_graph_id": item["parentReference"]["id"]
            }
        else:
            print("Something went terrible wrong in the 'get_values_data' function!")

    return folders, files, shared_folder_files

def get_permissions(shared_folders_files: dict, access_token: str) -> dict:
    '''
    Function that will accept a list of dictionaries, user_id and instance of a session from sqlalchemy.
    It will create batches of 20 requests (upper limit) and make post requests to the graph '$batch' endpoint to get all the permissions for files. 
    '''
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create nested list consisting of 20 request bodies each
    request_body_list = []
    body_len = 0
    batch_request = []
    for graph_id in shared_folders_files.keys():
        if body_len == 20:
            request_body_list.append(batch_request)
            batch_request = []
        batch_request.append({
            "id": graph_id,
            "method": "GET",
            "url": GET_PERMISSIONS.format(graph_id=graph_id)
        })
        body_len += 1
    request_body_list.append(batch_request) if batch_request else None
    
    # print(request_body_list)
    # print(batch_request)

    # Iterate through the list of request_body_list and make post requests to the permsissions endpoint for each request_body
    all_permissions = []
    for request_body in request_body_list:
        response = requests.post(
            url=GRAHP_BATCH_URL,
            json={"requests": request_body},
            headers=headers
        )
        # print(response.json())
        # print(request_body)
        all_permissions += response.json()["responses"] # adding responses to the permissions
    
    # Create a dictionary where the key is the graph_id and values are a set of emails that need to be checked in the db
    id_permissions_dict = defaultdict(dict)
    try:    
        for item in all_permissions:
            item_id = item["id"]
            # Get 'grantedToPermissionsV2' for each item
            granted = set()
            for value in item["body"]["value"]:
                if "grantedToIdentitiesV2" in value:
                    for gti in value["grantedToIdentitiesV2"]:
                        granted.add(gti["siteUser"]["email"])
            
            # Update the dictionary
            id_permissions_dict[shared_folders_files[item_id]][item_id] = {
                "granted_permission": granted
                # "type": shared_folders_files[item_id]
            }
            print("\n\nThere were no issues with the get_permissions function")
    except:
        print("\nThere were issues with the get_permissions function!!")
        print(shared_folders_files)
        # print(all_permissions) # ENSURE THAT ERRORS HERE ARE HANDLED!!!!

    return id_permissions_dict


def clean_folders_files_with_permissions(folder_file_data: dict, permissions: dict, id: int, db: Session):
    '''
    Function that will take in file and folder data in a dictionary, along with the permissions dictionary.
    It will then return two lists of dictionaries that can be directly fed into the repository functions that handle insertion into the user_files and user_folders table
    It requires the 'db', for calls to the db to retrieve the user_id's linked to the granted users (if they exist) and will add to a dict for rapid lookup and reduce redundant DB calls
    '''
    user_id_dict = {}
    folder_list = []
    file_list = []

    # HANDLING FOLDERS FIRST
    try:
        # Iterate through the list of tuples for folder data
        for folder in folder_file_data["folder"]:
            # check whether the graph_id matches any in the permissions dictionary
            if (graph_id := folder[1]) in permissions:
                print(True)
                print(graph_id)


    except: print("Something went terribly wrong trying to prep for the user_folder table :/")
    


def get_all_files(access_token: str, id: int, db:Session) -> str:
    '''
    This function will run as soon as a user accepts the invite request/after a workspace has been created.
    It will get all the files for the user using delta, to ensure a delta link is returned
    '''
    headers = {"Authorization": f"Bearer {access_token}"}
    # print(access_token)
    response = requests.get(
        url=INIT_GRAPH_GET,
        headers=headers
    )

    # Catch error, where user has no one drive files and returned is a 404 error
    if response.status_code == 404:
        return {
            "error": "no data!"
        }

    folder_data, file_data, shared_folders_files = {}, {}, {}
    while "@odata.nextLink" in (res := response.json()):
        folder_data, file_data, shared_folders_files = get_values_data(folders=folder_data, files=file_data, shared_folder_files=shared_folders_files, values=res["value"])
        
        response = requests.get(
            url = res["@odata.nextLink"],
            headers=headers
        )

    # FINAL DATA FETCH FROM GRAPH API
    # Get the delta link for the user
    try:
        delta_link = res["@odata.deltaLink"]
        auth_service.update_delta_link(id=id, delta_link=delta_link, db=db)
    except Exception as e:
        return {
            "status_code": 400,
            "error": f"{type(e).__name__} - {e}"
        }

    # Final update for folder and file data before database write
    folder_data, file_data, shared_folders_files = get_values_data(folders=folder_data, shared_folder_files=shared_folders_files, files=file_data, values=res["value"])
    
    # Insert into DB - HANDLE THE ERROR RESPONSE!!
    folder_file_response = repository.create_folders_files(folders=folder_data, files=file_data, db=db)
    # Insert into user-file and user-folder here for the current user_id - ensure that the above returns the id's of the files and folders created, so that an entry can be made for each in the next table!

    # Get all the users that have access to the folders and files for this user
    permissions_dict = get_permissions(shared_folders_files=shared_folders_files, access_token=access_token)

    # Go through folder and files and add them to the correct tables
    clean_folders_files_with_permissions(folder_file_data=folder_file_response["data"], permissions=permissions_dict, id=id, db=db)
    # repository.insert_user_folders(folders=folder_file_response["data"]["folder"], permissions_dict=permissions_dict, user_id=id, db=db)
    # repository.insert_user_files(files=folder_file_response["data"]["file"], permissions_dict=permissions_dict, db=db)

    return {"permissions_dict": permissions_dict}
    return {"status": folder_file_response["details"]}

def get_download_link_by_graph_id(graph_id: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        url=DOWNLOAD_URL_GET.format(graph_id=graph_id),
        headers=headers
    )
    if response.status_code == 200:
        return response.json()["@microsoft.graph.downloadUrl"]
    else:
        return None