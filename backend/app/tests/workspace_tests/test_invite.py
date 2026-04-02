import secrets
from app.invites.models import Invite
from app.invites.repository import add_invite, get_invite, get_invite_for_cooldown, get_invite_by_workspace_id, update_invite_used_value
from app.authentication.repository import delete_pending_user, get_pending_user_by_id
from app.authentication.models import PendingUser, User
from app.authentication import repository, service
from app.workspaces import models
from app.workspaces.repository import add_workspace, add_notification, add_user_workspace
from datetime import datetime, date, timedelta
from sqlalchemy import insert
from urllib.parse import quote
from io import BytesIO
from PIL import Image

# Creating test image 
def create_test_image():
    img = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.getvalue()

# Test a null email input
def test_null_email_input(db, client):
    image = create_test_image()
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace_insert = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email": None, "expiry_date": None},
    )
    response = client.send(request = req)
    
    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert db.query(Invite).count() == 0


# Test an invalid email input
def test_invalid_email_input(db, client):
    image = create_test_image()
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace_insert = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"invalid@example.com", "expiry_date":None},
    )
    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert db.query(Invite).count() == 0


# Test a valid email input (with no expiry date selected)
def test_valid_email_input(db, client):
    image = create_test_image()
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)
    
    workspace_insert = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":None},
    )
    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json().get("success") == "expiry"
    assert db.query(Invite).count() == 0


# Test a valid email with an expiry date selected
def test_valid_invite_request(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert=db.execute(workspace)
    
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"},
    )
    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json().get("success") == True
    assert db.query(Invite).count() == 1
    assert db.query(PendingUser).count() == 1
    assert db.query(models.pending_user_workspace).count() == 1


# Test sending an invite when a pending user with type 'request' has already been added to the database
def test_valid_invite_request(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    pending_user = insert(PendingUser).values(email="valid@example.com", type="request")
    res_2=db.execute(pending_user)

    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert=db.execute(workspace)
    
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"},
    )
    response = client.send(request = req)

    user = get_pending_user_by_id(db, res_2.inserted_primary_key[0])
    assert response.status_code == 200
    assert response.json().get("success") == True
    assert db.query(PendingUser).count() == 1
    assert user.type == "invite"


# Test invite record can be retrieved using its token
def test_retrieval_invite_record(db):
    image = create_test_image()
    token = str(secrets.token_hex(16))

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    admin_instance=db.execute(admin)

    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    workspace = add_workspace(db, "Test Workspace", image=image)
    add_invite(db, datetime.now(), datetime.today(), token, False, pending_user_instance.inserted_primary_key[0], workspace)

    invite = get_invite(db, token)
    assert invite is not None


# Test return statement with invalid invite record with invalid expiry date 
def test_expired_invite_record(db, client):
    image = create_test_image()
    token = str(secrets.token_hex(16))

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    admin_instance=db.execute(admin)

    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    workspace = add_workspace(db, "Test Workspace", image=image)
    add_invite(db, datetime.now(), date(2025, 3, 3), token, False, pending_user_instance.inserted_primary_key[0], workspace)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)

    assert response.headers["location"] == f"http://localhost:5173/invite-error/expired?date=2025-03-03&workspace={workspace.id}"
    assert db.query(PendingUser).count() == 1
    assert db.query(Invite).count() == 1


# Test if invite is clicked when the invite is not present in database
def test_invite_clicked_when_not_in_database(client):
    token = str(secrets.token_hex(16))
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    assert response.headers["location"] == "http://localhost:5173/workspace-joined"


# Test if invite is clicked when the invite used is true
def test_invite_clicked_when_used_is_true(db, client):
    image = create_test_image()
    token = str(secrets.token_hex(16))

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    admin_instance=db.execute(admin)

    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    workspace = add_workspace(db, "Test Workspace", image=image)
    add_invite(db, datetime.now(), date(2025, 3, 3), token, True, pending_user_instance.inserted_primary_key[0], workspace)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    assert response.headers["location"] == "http://localhost:5173/workspace-joined"


# Test return statement with valid invite
def test_valid_invite(db, client):
    image = create_test_image()
    token = str(secrets.token_hex(16))
    
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    admin_instance=db.execute(admin)

    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    workspace = add_workspace(db, "Test Workspace", image=image)
    add_invite(db, datetime.now(), date(2030, 3, 3), token, False, pending_user_instance.inserted_primary_key[0], workspace)

    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    next_url = "/dashboard?toast=signup"
    redirect_url = f"http://localhost:8000/auth/sign-in?next={quote(next_url)}&signup=true&role=2&workspace_id={workspace.id}"
    assert response.headers["location"] == redirect_url
    assert response.status_code == 302
    assert db.query(PendingUser).count() == 1
    assert db.query(Invite).count() == 1


# Test getting pending user by their id and deleting pending user method
def test_delete_pending_user_by_getting_id(db):
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    res = db.execute(insert_statement)
    user = get_pending_user_by_id(db, res.inserted_primary_key[0])
    delete_pending_user(db, user.user_id)
    assert db.query(PendingUser).first() is None


# Test that the latest invite gets pulled based on the workspace and the user
def test_method_get_invite_for_cooldown(db):
    image = create_test_image()
    token = str(secrets.token_hex(16))
    time = datetime.now().replace(microsecond=0)
    latest_time = time + timedelta(days=3)

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    admin_instance=db.execute(admin)

    pending_user_instance = PendingUser(email="JohnSmith1@hotmail.com", type="invite")
    db.add(pending_user_instance)
    db.flush()

    workspace = add_workspace(db, "Test Workspace", image=image)
    add_invite(db, time, date(2030, 3, 3), token, False, pending_user_instance.user_id, workspace)
    add_invite(db, time + timedelta(days=2), date(2030, 3, 3), token, False, pending_user_instance.user_id, workspace)
    add_invite(db, latest_time, date(2030, 3, 3), token, False, pending_user_instance.user_id, workspace)

    invite = get_invite_for_cooldown(db, workspace, pending_user_instance)

    assert invite.created_at == latest_time
    assert invite.user_id == pending_user_instance.user_id
    assert invite.workspace_id == workspace.id

# Test return statement when sending 2 invites back-to-back
def test_return_statement_with_invalid_cooldown(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert=db.execute(workspace)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # invite 1
    invite_1 = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"},
    )
    response = client.send(request = invite_1)

    # invite 2
    invite_2 = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"},
    )
    response = client.send(request = invite_2)

    assert response.json().get("success") == "cooldown"
    assert db.query(Invite).count() == 1
    assert db.query(PendingUser).count() == 1


# Test return statement when sending an invite to the same email as the admin sending the email
def test_return_statement_with_same_email_as_admin(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="valid@example.com", email="valid@example.com", refresh="ms-refresh".encode(), oid=oid, role="admin")
    res=db.execute(insert_statement)

    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_insert=db.execute(workspace)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/invite/send-invite",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"email":"valid@example.com", "expiry_date":"2030-03-01T14:35:10.123456"},
    )
    response = client.send(request = req)

    assert response.json().get("success") == "admin"
    assert db.query(Invite).count() == 0
    assert db.query(PendingUser).count() == 0


# Testing the create notification route
def test_request_join_workspace_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="valid@example.com", refresh="me-refresh".encode(), email="valid@example.com", oid=oid, role="admin")
    res=db.execute(insert_statement)

    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_instance = db.execute(workspace)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/request-join-workspace",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"title":"Test title", "body":"Test body", "workspace_id":workspace_instance.inserted_primary_key[0]},
    )
    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == True
    assert db.query(models.Notification).count() == 1


# Testing the route to get all notifications for a user
def test_get_all_notifications_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="valid@example.com", refresh="me-refresh".encode(), email="valid@example.com", oid=oid, role="admin")
    res=db.execute(insert_statement)
    
    workspace = insert(models.Workspace).values(name="Test Workspace", image=image)
    workspace_instance = db.execute(workspace)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Notifications
    n_1 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])
    n_2 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])
    n_3 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])

    req = client.build_request(
        method="get",
        url="/workspace/get-notifications",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    expected_notifications = [
    {
        "title": n.title,
        "body": n.body,
        "datetime": n.datetime.isoformat(),
        "id": n.id,
        "user_id": n.user_id,
    }
    for n in [n_1, n_2, n_3]
    ]

    response = client.send(request = req)
    data = response.json()
    assert db.query(models.Notification).count() == 3
    assert data == expected_notifications


# Testing deleting a user's notification 
def test_delete_notification_route(db, client):

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="valid@example.com", refresh="me-refresh".encode(), email="valid@example.com", oid=oid, role="admin")
    res=db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    # Notifications
    n_1 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])
    n_2 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])
    n_3 = add_notification(db, "title", "body", datetime.now(), res.inserted_primary_key[0])

    response = client.post(
        "/workspace/delete-notification",
        headers={"Authorization": f"Bearer {access}"},
        json={"notification_id": n_1.id}
    )

    expected_notifications = [
    {
        "title": n.title,
        "body": n.body,
        "datetime": n.datetime.isoformat(),
        "id": n.id,
        "user_id": n.user_id,
    }
    for n in [n_2, n_3]
    ]

    assert db.query(models.Notification).count() == 2
    assert response.json() == expected_notifications


# Get invite by workspace id
def test_get_invite_by_workspace_id(db):
    image = create_test_image()
    token = str(secrets.token_hex(16))
    time = datetime.now().replace(microsecond=0)

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace = add_workspace(db, "Test Workspace", image=image)
    
    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    add_invite(db, time, date(2030, 3, 3), token, False, pending_user_instance.inserted_primary_key[0], workspace)
    invite = get_invite_by_workspace_id(db, workspace.id)

    assert invite is not None


# Update invite used value
def test_update_invite_used_value(db):
    image = create_test_image()
    token = str(secrets.token_hex(16))
    time = datetime.now().replace(microsecond=0)

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    workspace = add_workspace(db, "Test Workspace", image=image)

    pending_user = insert(PendingUser).values(email="JohnSmith1@hotmail.com", type="invite")
    pending_user_instance=db.execute(pending_user)

    invite = add_invite(db, time, date(2030, 3, 3), token, False, pending_user_instance.inserted_primary_key[0], workspace)
    update_invite_used_value(db, invite.invite_id)

    assert invite.used == True








    











