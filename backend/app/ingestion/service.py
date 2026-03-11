from msal import ConfidentialClientApplication
from ..core.security import decrypt_refresh
from ..core.config import SCOPES
from . import repository
from ..authentication import service as auth_service

def get_user_access(application: ConfidentialClientApplication, user, db) -> str | None:
    # This is to get the access token for users - THAT ARE ALREADY LOGGED IN!
    user_details = auth_service.check_get_by_id(user.user_id, db)
    access_token = None
    
    if user_details:
        print(user_details.email)
        account = application.get_accounts()
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

# def get_all_files(token)


