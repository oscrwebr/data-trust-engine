from msal import ConfidentialClientApplication
import requests, json

from ..core.security import decrypt_refresh
from ..core.config import SCOPES
from . import repository
from ..authentication import service as auth_service
from .schemas import Folder, File


INIT_GRAPH_GET = "https://graph.microsoft.com/v1.0/me/drive/root/delta?$select=id,name,lastModifiedDateTime,parentReference,file,folder,webUrl,shared"



def get_user_access(application: ConfidentialClientApplication, user, db) -> str | None:
    # This is to get the access token for users - THAT ARE ALREADY LOGGED IN!
    user_details = auth_service.check_get_by_id(user.user_id, db)
    access_token = None
    
    if user_details:
        print(user_details.email)
        account = application.get_accounts(username=user_details.username)
        print(f"This is the account: {account}\n\n")
        if account:
            access_token = application.acquire_token_silent(scopes=SCOPES, account=account[0])["access_token"]
            # print(access_token)
        else:
            print("need to get refresh and then follow through with access token flow!")
            account = application.acquire_token_by_refresh_token(refresh_token=decrypt_refresh(user_details.refresh), scopes=SCOPES)
            # print(account)
            access_token = account["access_token"]
    
    return access_token


def get_values_data(folders: dict, files: dict, values: list[dict]):
    '''
    Function that will take in two dictionaries that containing retrieved data for both folders and files as well as a list of dictionaries returned by the json response from Graph API.
    It will then return two dictionaries 'folders' and 'files'.
    - 'folders' - Entries will consist of a key made from the graph_id and value that is an instance of the Folder class from the related schema
    - 'files' - Entries will consist of a key made from the graph_id and value that is an instance of the File class from the related schema
    '''

    for item in values:
        print(f"\n\n{item}\n\n{type(item)}\n\n")
        if "folder" in item: # This means that the item is a folder
            # This is in case the folder is the root folder itself
            # parent_id = parent_ref_id if (parent_ref_id := item["parentReference"]["id"]) else item["parentReference"]["driveId"]
            if "id" in item["parentReference"]:
                parent_id = item["parentReference"]["id"]
            else:
                parent_id = item["parentReference"]["driveId"]

            id = item["id"]
            folders[id] = Folder(
                graph_id=id,
                name=item["name"],
                web_url=item["webUrl"],
                parent_id=parent_id
            )
        elif "file" in item:
            id = item["id"]
            item_name = item["name"]
            # Sometimes hash doesn't exist
            hash_exists = True if item["file"]["hashes"] else False

            files[id] = File(
                graph_id=id,
                name=item_name,
                extension=item_name.split(".")[-1],
                hash=next(iter(item["file"]["hashes"].values())) if hash_exists else None,
                hash_type=next(iter(item["file"]["hashes"])) if hash_exists else None,
                last_modified=item["lastModifiedDateTime"],

                web_url=item["webUrl"],
                parent_id=item["parentReference"]["id"]
            )
        else:
            print("Something went terrible wrong in the 'get_values_data' function!")
    return folders, files

def get_all_files(access_token: str) -> str:
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
    folder_data, file_data = {}, {}
    while "@odata.nextLink" in (res := response.json()):
        folder_data, file_data = get_values_data(folders=folder_data, files=file_data, values=response.json()["value"])
        
        response = requests.get(
            url = res["@odata.nextLink"],
            headers=headers
        )

    # Final data fetch from graph
    folder_data, file_data = get_values_data(folders=folder_data, files=file_data, values=response.json()["value"])

    return {
        "data": {
            "folder_data": folder_data,
            "file_data": file_data
        }

    }


