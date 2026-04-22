from msal import ConfidentialClientApplication
from sqlalchemy.orm import Session
from app.authentication import repository
from datetime import datetime, timezone, timedelta
import requests

from ..core.config import SCOPES
from ..core.security import create_refresh_token, create_access_token, hash_user_refresh_token, encrypt_refresh, decrypt_refresh
from app.core.celery_worker import celery
from app.core.database import SessionLocal
from app.ingestion.service import get_set_all_graph_files
from app.workspaces.repository import add_notification, get_workspace_by_workspace_id, add_user_workspace
from app.invites.repository import get_invite_by_token
from app.roles.repository import migrate_pending_roles
from app.authentication.repository import get_pending_user_by_email, delete_pending_user
from app.authentication.models import User

DRIVE_DATA_GRAPH_URL = "https://graph.microsoft.com/v1.0/me/drive?$select=id"

def create_user(db, details: dict, refresh: str, ms_access_token: str, role: str):
    split_name = details["name"].split()
    firstname, surname = split_name[0], split_name[-1]
    enc_refresh = encrypt_refresh(refresh)
    # Get the DriveId - IF there is an error, maybe log it for future so that it can be fetched at another time? This should be the only major potential point of failure if user creation reaches this stage
    drive_id = get_drive_id(access_token=ms_access_token)

    email = details["email"]

    user = repository.create_user(
        db=db,
        firstname=firstname,
        surname=surname,
        username=details["preferred_username"],
        email=email,
        oid=details["oid"],
        refresh=enc_refresh,
        driveId=drive_id,
        role=role
    )

    # Handle ingestion with celery - in the background and sets up a queue, incase of multiple signup and inturn ingestion requests at once
    _ = setup_ingestion_celery.delay(ms_access_token, user.user_id)

    return user

# Method to handle user creation for anyone who has accepted an invite
def handle_user_creation_after_invite(db: Session, user: User, workspace_id: int, token: str):
    invite = get_invite_by_token(db, token)
    pending_user = repository.get_pending_user_by_id(db, invite.user_id) if invite else None
    
    migrate_pending_roles(db, pending_user.user_id, user.user_id)
    delete_pending_user(db, pending_user.user_id)
    add_user_workspace(db, workspace_id, user.user_id)
    workspace = get_workspace_by_workspace_id(db, workspace_id)
    users = workspace.user
    for user in users:
        if(user.role == "admin"):
            user_id = user.user_id

    add_notification(db, "Employee Accepted Invite", f"{user.firstname} {user.surname} accepted their invite request to join your workspace.", datetime.now(), user_id)


@celery.task
def setup_ingestion_celery(ms_access_token, user_id):
    db = SessionLocal()
    try:
        return get_set_all_graph_files(ms_access_token, user_id, db)
    finally:
        db.close()

def check_get_by_id(id: int, db):
    user = repository.get_by_id(id, db)
    return user if user else None

def check_get_by_oid(oid: str, db):
    # print(oid)
    user = repository.get_by_oid(oid, db)
    # print(f"User details:\nFirstname: {res.firstname}\nSurname: {res.surname}\nemail: {res.email}") if res else print("There is nothing there!")
    return user if user else None

def check_get_by_email(email: str, db: Session):
    user = repository.get_by_email(email, db)
    return user if user else None

def test_route(id: int, db):
    user = repository.get_by_id(user_id=id, db=db)
    return user if user else None

def create_access_refresh(db: Session, data: dict, refresh_family_id: int | None=None):
    refresh_token = create_refresh_token()
    access_token = create_access_token(data=data).access_token
    hashed_token = hash_user_refresh_token(refresh_token.opaque_token)
    if not refresh_family_id:
        new_refresh_family = repository.create_refresh_family(db=db) # PUT ALL OF THIS INTO ONE LINE!!
        print(new_refresh_family.is_revoked)
        refresh_family_id = new_refresh_family.refresh_family_id
    
    new_entry = repository.create_refresh(db=db, uid=data['userId'], hashed_token=hashed_token, expiry=refresh_token.expiry_date, refresh_family_id=refresh_family_id, access_token=access_token)
    return access_token, refresh_token, new_entry
    
def refresh_flow(db, client_refresh: str, current_time: datetime):
    """
    - This function will handle generating new access tokens and refresh tokens
    - It will also handle the rotation of access tokens
    - It will allow a grace period of 30 seconds once a new refresh has been generated
    """
    hashed_token = hash_user_refresh_token(client_refresh)
    refresh_details = repository.get_refresh_details_by_token(db=db, hashed_token=hashed_token)
    return_dict = {}
    # print(f"\n\n This is the current time: {current_time}\n\n")
    # Check if anything was returned
    if not refresh_details:
        print("No Details!")
        return return_dict
    # Check if there is a family, and whether it has been revoked
    if refresh_family_id := refresh_details.refresh_family_id: # checks whether there is anything in that column for the row
        refresh_family = repository.get_by_refresh_family_id(db=db, refresh_family_id=refresh_family_id)
        if refresh_family.is_revoked:
            print("This token family is revoked!")
            return return_dict
        if refresh_family.is_disconnected:
            repository.revoke_refresh_family(db, refresh_details.refresh_family_id)
            print("this family is disconnected! It is now revoked!")
            return return_dict

    # Check that the token has not been replaced by another token yet
    if refresh_details.replaced_by:
        # These are checks incase the client has sent multiple requests at once within the grace period of 30 seconds
        if replaced_at := refresh_details.replaced_at:
            # print(f"\n\nreplaced at: {replaced_at.replace(tzinfo=timezone.utc)}\nCurrent time: {current_time}\n\n")
            if replaced_at.replace(tzinfo=timezone.utc) + timedelta(seconds=30) > current_time:
                print("This is within accepted boundaries - return the access token to the user and don't rotate refresh token")
                return_dict["access_token"] = refresh_details.access_token
                return return_dict
            else:
                print("This is bad - kill session chain immediately!!!")
                # Revoke refresh_family
                repository.revoke_refresh_family(db, refresh_details.refresh_family_id)
                return return_dict
    
    # Check the expiry - this should be cleared daily, but that is just garbage collection. This must be checked.
    if refresh_details.expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        print("Token has expired - redo authentication workflow")
        # Revoke refresh_family
        repository.revoke_refresh_family(db, refresh_details.refresh_family_id)
        return return_dict
    # ISSUING NEW ACCESS TOKEN AND REFRESH TOKEN
    uid = repository.get_uid_from_refresh_id(db=db, refresh_id = refresh_details.refresh_id)
    user = repository.get_by_id(user_id=uid, db=db)
    access_token, refresh_token, new_entry_details = create_access_refresh(db=db, data={"userId": uid, "role": user.role}, refresh_family_id=refresh_details.refresh_family_id)
    # UPDATING PREVIOUS REFRESH TOKEN
    repository.update_prev_refresh_entry(db=db, prev_id=refresh_details.refresh_id, new_id=new_entry_details.refresh_id)
    return_dict = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return return_dict

def rotate_ms_refresh(id: int, refresh_token: str, db:Session):
    repository.update_ms_refresh(id, refresh_token, db)

def update_delta_link(id: int, delta_link: str, db:Session):
    repository.update_delta_link(id, delta_link, db)

def get_user_access(application: ConfidentialClientApplication, user_id, db:Session) -> str | None:
    # This is to get the access token for users - THAT ARE ALREADY LOGGED IN!
    user_details = check_get_by_id(user_id, db)
    access_token = None
    
    if user_details:
        account = application.get_accounts(username=user_details.username)
        if account:
            tokens = application.acquire_token_silent(scopes=SCOPES, account=account[0])
            access_token = tokens["access_token"]
            # Rotate the refresh token in the DB
            enc_refresh = encrypt_refresh(tokens["refresh_token"])
            rotate_ms_refresh(user_id, enc_refresh, db)

        else:
            account = application.acquire_token_by_refresh_token(refresh_token=decrypt_refresh(user_details.refresh), scopes=SCOPES)
            access_token = account["access_token"]
            # Rotate the refresh token in the DB
            enc_refresh = encrypt_refresh(account["refresh_token"])
            rotate_ms_refresh(user_id, enc_refresh, db)
    else:
        return None

    return access_token

def get_drive_id(access_token: str):
    '''
    Function that will get the DriveId for the user
    '''
    # GET request to retrieve the drive data
    response = requests.get(url=DRIVE_DATA_GRAPH_URL,
                 headers={"Authorization": f"Bearer {access_token}"})
    drive_data = response.json()

    # Extracting the driveId from the response and updating user table in the DB
    if "id" in drive_data:
        return drive_data["id"]
        # repository.update_user_drive_data(user_id=id, drive_id=drive_data["id"], db=db)
    else:
        print("There was an fethching the drive data for the user!")
        return None
    
def get_access_with_drive_id(application: ConfidentialClientApplication, drive_id: str, db) -> str|None:
    user = repository.get_user_id_by_drive_id(drive_id, db)
    if not user:
        return None
    return get_user_access(application=application, user_id=user.user_id, db=db)

def delete_user(db: Session, user_id: int):
    repository.delete_user(db, user_id)
    return True

def reject_pending_user(db: Session, user_id: int):
    repository.delete_pending_user(db, user_id)
    return True

def get_pending_by_id(db: Session, user_id: int):
    return repository.get_pending_user_by_id(db, user_id)

def get_pending_by_email(db: Session, email: str):
    return repository.get_pending_user_by_email(db, email)

def add_pending_user(db: Session, email: str, type: str):
    return repository.add_user(db, email, type)

def log_out_flow(db: Session, client_refresh: str, current_time: datetime):
    '''
    Function that will handle user's when they log out. 
    - Checks that refresh token is the latest by checking whether it has been replaced ('by' and 'at')
    - Checks that the associated refresh_family is not revoked and is not also logged out
    - If there are multiple logouts with the same refresh token - it will allow a grace period of 30 seconds in case of repeat requests to log out by the client - if > 30 seconds, the refresh family will be revoked
    '''
    # Getting the refresh token by from the string obtained by the visiting user
    hashed_token = hash_user_refresh_token(client_refresh)
    refresh_details = repository.get_refresh_details_by_token(db=db, hashed_token=hashed_token)

    # Checking that this is the latest version of the refresh token - if not, time delay doesn't matter here. The refresh family must be revoked!
    if refresh_details.replaced_by:
        repository.revoke_refresh_family(db, refresh_details.refresh_family_id)
        return
    # Checking whether the token has been revoked
    refresh_family_details = repository.get_by_refresh_family_id(db=db, refresh_family_id=refresh_details.refresh_family_id)
    if refresh_family_details.is_revoked:
        return
    # Checking whether the token has been disconnected
    if refresh_family_details.is_disconnected:
        # Check whether the token has been disconnected in the last 30 seconds
        if refresh_details.replaced_at.replace(tzinfo=timezone.utc) + timedelta(seconds=30) > current_time:
            return
        # This means that someone is reusing an old refresh token to logout - must revoke refresh_family!
        repository.revoke_refresh_family(db, refresh_details.refresh_family_id)
        return
    # If this point is reached, all checks have passed - can update the replaced_at time and set the refresh_family 'is_disconnected' value to true
    repository.disconnect_refresh_family(db=db, refresh_family_id=refresh_details.refresh_family_id)
    repository.update_refresh_replaced_at(db=db, refresh_id=refresh_details.refresh_id)