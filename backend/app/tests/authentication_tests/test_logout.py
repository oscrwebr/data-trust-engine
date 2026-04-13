from sqlalchemy import insert, select, update
import requests, json
from datetime import datetime, timezone, timedelta

from app.authentication.models import User, RefreshFamily, Refresh
from app.authentication import repository, service

# Test that if a user doesn't have a refresh token, 200 error is returned, as nothing needs to happen
def test_200_if_no_refresh_token(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"}
    )
    response = client.send(request = req)
    # ASSERTIONS
    # Ensure that 200 is the response status code
    assert response.status_code == 200

# Test that if a user has a refresh token that is valid, then the corresponding refresh_family entry gets disconnected
def test_valid_refresh_gets_disconnected(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    assert refresh_family.is_disconnected == False
    assert refresh_family.is_revoked == False

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)
    # Getting the updated values for the refresh_family entry
    select_statement = select(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id)
    latest_refresh = db.execute(select_statement).scalar_one()

    # ASSERTIONS
    assert latest_refresh.is_disconnected == True
    assert latest_refresh.is_revoked == False


# Test that if a user logs out with the same token within the 30 second grace, they are returned with a 200 staus_code
def test_200_returned_if_multiple_log_out_in_30_seconds(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    assert refresh_family.is_disconnected == False
    assert refresh_family.is_revoked == False

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )

    # making second request with the same dte_refresh_token 
    req_2 = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)
    response_2 = client.send(request = req_2)
    
    # Getting the updated values for the refresh_family entry
    select_statement = select(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id)
    latest_refresh = db.execute(select_statement).scalar_one()

    # ASSERTIONS
    assert response_2.status_code == 200
    assert latest_refresh.is_disconnected == True
    assert latest_refresh.is_revoked == False
    
# Test that if a user logs out with the same token outside of the 30 second grace, the refresh_family is revoked
def test_revoked_if_multiple_log_outs_outside_30_seconds(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    assert refresh_family.is_disconnected == False
    assert refresh_family.is_revoked == False

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )

    # making second request with the same dte_refresh_token 
    req_2 = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    response = client.send(request = req)
    
    # Updating the refresh_token replaced at time
    update_statement = update(Refresh).where(Refresh.token == refresh.hashed_ot).values(replaced_at = (datetime.now(timezone.utc)-timedelta(days=1)))
    db.execute(update_statement)
    db.commit()

    response_2 = client.send(request = req_2)
    
    # Getting the updated values for the refresh_family entry
    select_statement = select(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id)
    latest_refresh = db.execute(select_statement).scalar_one()

    # ASSERTIONS
    assert response_2.status_code == 200
    assert latest_refresh.is_disconnected == True
    assert latest_refresh.is_revoked == True

# Test that if a refresh token is not the latest token, then the associated family gets revoked
def test_old_refresh_causes_family_revokation(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    assert refresh_family.is_disconnected == False
    assert refresh_family.is_revoked == False

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # making a request with the dte_refresh_token 
    req = client.build_request(
        method="get",
        url="/auth/token/refresh",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    client.send(request=req)
    
    # Ensure that there is only one value there, as test is dependent on this being True
    select_statement = select(Refresh)
    refresh_entries = db.execute(select_statement).scalars().all()
    assert len(refresh_entries) == 2

    # Updating the refresh_token replaced at time
    update_statement = update(Refresh).where(Refresh.refresh_id == refresh_entries[0].refresh_id).values(replaced_at = (datetime.now(timezone.utc)-timedelta(days=1)))
    db.execute(update_statement)
    db.commit()

    # Ensure the refresh_family isn't already revoked
    select_statement = select(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id)
    latest_refresh = db.execute(select_statement).scalar_one()

    assert latest_refresh.is_revoked == False

    # Make request to logout
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    res = client.send(request=req)

    # ASSERTIONS
    # Getting the updated values for the refresh_family entry
    latest_refresh = db.execute(select_statement).scalar_one()
    assert latest_refresh.is_revoked == True
    assert latest_refresh.is_disconnected == False

# Test that if a refresh_family is already revoked, nothing changes and it DOESN'T get disconnected
def test_revoked_refresh_does_not_get_disconnected(db, client):
    ## SETTING UP THE TEST
    # Insert the test user
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode() , role="admin")
    res = db.execute(insert_statement)

    # Create test refresh_family entry
    refresh_family = repository.create_refresh_family(db)

    # Update refresh family and revoke it
    update_statement = update(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id).values(is_revoked=True)
    db.execute(update_statement)
    db.commit()

    # Creating access and refresh tokens for the new user with the 'create_access_refresh()' function
    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

     # Make request to logout
    req = client.build_request(
        method="post",
        url="/auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"dte_refresh_token": refresh.opaque_token}
    )
    res = client.send(request=req)

    # Getting the latest changes to the refresh_family since the request to logout
    refresh_family_select = select(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family.refresh_family_id)
    refresh_family_latest = db.execute(refresh_family_select).scalar()

    # Assert that there were no errors with the request
    assert res.status_code == 200
    assert refresh_family_latest.is_disconnected == False
    assert refresh_family_latest.is_revoked == True
