from app.core import config
from sqlalchemy import insert, select, update, func, desc
from datetime import datetime, timezone, timedelta

from app.authentication import models, service, repository

# This tests whether an unauthenticated user can access a protected endpoint
def test_unauthenticated_user_cannot_access_protected_endpoints(client):
    response = client.get("/auth/test")
    assert response.status_code == 401

# This tests whether the sign in route works with a 'next' parameter that doesn't start with a '/'
def test_sign_in_with_next_query_parameter_omitting_forward_slash(client):
    response = client.get("/auth/sign-in?next=test")
    assert response.status_code == 403

# This tests whether the success route will accept a request without a session cookie
def test_success_without_session(client):
    response = client.get("/auth/success/")
    assert response.status_code == 400

# This tests whether the /success/ endpoint will redirect to the 422 error page if there is an error in the query parameters
def test_success_with_error_in_query_params(client):
    response = client.get("/auth/success/?error=access_denied")
    assert response.url == f"{config.FRONTEND_BASE_URL}/error/422"

# This tests whether the 'check_exists' function works correctly in 'authentication/service.py' when the user exists
def test_user_returned_when_they_exist_in_db(db):
    # Creating the user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    db.execute(insert_statement)
    assert db.query(models.User).count() == 1 # incase the user doesn't get added

    # Checking the service works
    response = service.check_exists(oid=oid, db=db)
    assert response
    assert response.oid == oid

# This tests whether the 'check_exists' function works correctly in the 'authentication/service.py' when the user doesn't exist
def test_none_returned_when_user_does_not_exist(db):
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    assert db.query(models.User).count() == 0
    response = service.check_exists(oid=oid, db=db)
    assert response == None

# This tests whether the '/auth/token/refresh' endpoint raises a 403 error if the user doesn't have a refresh token in the header
def test_403_if_no_refresh_present(client):
    response = client.get("/auth/token/refresh")
    assert response.status_code == 403

# This tests whether an access token is generated and refresh token is rotated if the user has a valid refresh token
def test_auth_and_refresh_token_rotated_if_user_has_valid_refresh(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    select_statement = select(models.Refresh.token, models.Refresh.access_token).order_by(desc(models.Refresh.refresh_id)).limit(1)
    select_response = db.execute(select_statement).all()[0]
    hashed_rotated_token, new_access_token = select_response[0], select_response[1]
    new_browser_token = response.cookies.get("dte_refresh_token")

    # Assertions
    assert "access_token" in response.json() # This checks that there is an access_token in the json response
    assert response.json()["access_token"] == new_access_token # This ensure that the access token is equal to the latest access token that was generated
    assert hashed_rotated_token == service.hash_user_refresh_token(new_browser_token) # This ensure that the current refresh token in the browser is the same as the latest one rotated in the database

# This tests that if a refresh token is valid, when it gets replace, then the previous refresh token entry in the refresh table should have its 'replaced_by' and 'replaced_at' columns updated
def test_replaced_by_and_at_updated_if_refresh_token_is_valid(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    # get replaced_at and replaced_by values before request is made
    
    select_refresh_details_statement = select(models.Refresh).where(models.Refresh.token == refresh.hashed_ot)
    init_refresh = db.execute(select_refresh_details_statement).scalar()
    init_refresh_id = init_refresh.refresh_id
    init_refresh_replaced_by = init_refresh.replaced_by
    init_refresh_replaced_at = init_refresh.replaced_at

    # Initial assertions
    assert init_refresh_replaced_by == None
    assert init_refresh_replaced_at == None

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    # get the latest refresh token id
    latest_refresh_token = response.cookies.get("dte_refresh_token")
    hashed_refresh = service.hash_user_refresh_token(latest_refresh_token)
    select_latest_refresh_statement = select(models.Refresh.refresh_id).where(models.Refresh.token == hashed_refresh)
    latest_refresh_id = db.execute(select_latest_refresh_statement).scalar()

    # get the previous refresh tokens details again
    init_refresh_2 = db.execute(select_refresh_details_statement).scalar()
    
    # Assertions
    assert init_refresh_2.replaced_by == latest_refresh_id  # Ensure that replaced by is correct
    assert init_refresh_2.replaced_at != None # ensure that replaced at has a value that is non-null

# This tests to ensure that if a refresh token is revoked a 401 error is returned
def test_401_raised_if_refresh_family_is_revoked(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)
    # Update refresh_family entry to be revoked
    repository.revoke_refresh_family(db, refresh_family.refresh_family_id)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    assert response.status_code == 401

# This tests that if tokens were rotated in the last 30 seconds, refresh tokens should not be rotated, and the same access token should be returned to the client
def test_no_rotation_and_same_access_token_returned_if_requests_within_30_seconds(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    select_statement = select(models.Refresh.token, models.Refresh.access_token).order_by(desc(models.Refresh.refresh_id)).limit(1)
    select_response = db.execute(select_statement).all()[0]
    hashed_rotated_token, rotated_access_token = select_response[0], select_response[1]
    response_one = response.cookies.get("dte_refresh_token")

    # Assertions
    assert "access_token" in response.json() # This checks that there is an access_token in the json response
    assert response.json()["access_token"] == rotated_access_token # This ensure that the access token is equal to the latest access token that was generated
    assert hashed_rotated_token == service.hash_user_refresh_token(response_one) # This ensure that the current refresh token in the browser is the same as the latest one rotated in the database

    # Getting count for refresh table before second request
    count_refresh_before = db.query(models.Refresh).count()
    
    # Making second request with old refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    # getting count for refresh table after second request
    count_refresh_after = db.query(models.Refresh).count()

    assert response.json()["access_token"] == rotated_access_token # Ensure that the latest access token hasn't been changed since the first response
    assert count_refresh_before == count_refresh_after # Ensure there are no new entries in the 'refresh' table

# This tests that if a refresh token has expired, a 401 error is returned
def test_401_returned_if_refresh_expired(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    select_statement = select(models.Refresh)
    refresh_id = db.execute(select_statement).scalar().refresh_id

    # updating the refresh token expiry to the past
    new_date = datetime.now(timezone.utc) - timedelta(days=1)
    update_statement = update(models.Refresh).where(models.Refresh.refresh_id == refresh_id).values(expiry=new_date)
    db.execute(update_statement)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)
    
    # assertion that the status code is 401
    assert response.status_code == 401

# This tests that if a refresh token has expired, corresponding refresh_family 'is_revoked' column == True
def test_is_revoked_is_true_if_refresh_expired(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(models.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

    select_statement = select(models.Refresh)
    select_statement_res = db.execute(select_statement).scalar()
    refresh_id = select_statement_res.refresh_id

    # updating the refresh token expiry to the past
    new_date = datetime.now(timezone.utc) - timedelta(days=1)
    update_statement = update(models.Refresh).where(models.Refresh.refresh_id == refresh_id).values(expiry=new_date)
    db.execute(update_statement)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)

    select_is_revoked_statement = select(models.RefreshFamily.is_revoked).where(models.RefreshFamily.refresh_family_id == select_statement_res.refresh_family_id)
    
    assert db.execute(select_is_revoked_statement).scalar() == True