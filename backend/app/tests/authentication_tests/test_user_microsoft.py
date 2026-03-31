from sqlalchemy import insert, select

from app.authentication.models import User
from app.authentication.service import get_user_access
from app.core.security import encrypt_refresh, decrypt_refresh

class FakeMsal():
    def get_accounts(self, *args, **kwargs):
        return ["This is the user account!"]
    def acquire_token_silent(self, *args, **kwargs):
        return {
            "access_token": "fake-ms-access-token",
            "refresh_token": "fake-ms-refresh-token"
        }
    def acquire_token_by_refresh_token(self, *args, **kwargs):
        return {
            "access_token": "fake-ms-access-token_from_refresh",
            "refresh_token": "fake-ms-refresh-token_from_refresh"
        }
class FakeMsal_no_cache():
    def get_accounts(self, *args, **kwargs):
        return None
    def acquire_token_by_refresh_token(self, *args, **kwargs):
        return {
            "access_token": "fake-ms-access-token_from_refresh",
            "refresh_token": "fake-ms-refresh-token_from_refresh"
        }

# Test to ensure that when files need to be pulled via Graph API, access token can be retrieved for user that is in cache
def test_access_token_retrieval_for_cached_user(db):
    fake_msal = FakeMsal()
    # create data for user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()
    # proves refresh is what was inserted
    assert decrypt_refresh(user.refresh) == "ms-refresh-token"

    # call the service for getting access_token from user_id
    access_token = get_user_access(fake_msal, user.user_id, db)
    assert access_token == "fake-ms-access-token"
    
    # ensure that the refresh token in the db for the user is rotated!!!
    select_statement = select(User).where(User.user_id == user.user_id)
    updated_user = db.execute(select_statement).scalar_one()
    assert decrypt_refresh(updated_user.refresh) == "fake-ms-refresh-token"

# Test ensuring that Microsoft access token can be retrieved to users even in they aren't in the token cache of the MSAL library (in case of things like server reloads)
def test_access_token_retrieval_for_non_cached_user(db):
    fake_msal = FakeMsal_no_cache()
    # create data for user that is being tested
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="johnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", refresh=encrypt_refresh("ms-refresh-token"), oid=oid, role="employee").returning(User)
    user = db.execute(insert_statement).scalar_one()
    # proves refresh is what was inserted
    assert decrypt_refresh(user.refresh) == "ms-refresh-token"

    # call the service for getting access_token from user_id
    access_token = get_user_access(fake_msal, user.user_id, db)
    assert access_token == "fake-ms-access-token_from_refresh"
    
    # ensure that the refresh token in the db for the user is rotated!!!
    select_statement = select(User).where(User.user_id == user.user_id)
    updated_user = db.execute(select_statement).scalar_one()
    assert decrypt_refresh(updated_user.refresh) == "fake-ms-refresh-token_from_refresh"
    