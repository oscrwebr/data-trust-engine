from app.workspaces import models as workspace_model
from app.authentication import models as auth_model, repository, service
from app.workspaces.repository import add_user_workspace, add_pending_user_workspace, add_notification, get_workspace_by_workspace_id, add_workspace
from app.roles.repository import create_role
from sqlalchemy import insert, select, desc
from datetime import datetime

from io import BytesIO
from PIL import Image

# Creating test image 
def create_test_image():
    img = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.getvalue()

# Testing add_workspace function to make sure record is inserted
def test_add_workspace_record(db):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(admin)

    workspace = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    db.execute(workspace)

    assert db.query(workspace_model.Workspace).count() == 1 

# Testing /create-workspace endpoint with null name
def test_create_workspace_null_name(db, client):
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/create-workspace",
        headers={"Authorization": f"Bearer {access}"}, 
        data={"name": "null"}, 
        files={"image": ("test.png", BytesIO(b"fake image content"), "image/png")},
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == "name"
    assert db.query(workspace_model.Workspace).count() == 0 


# Testing /create-workspace endpoint with null image
def test_create_workspace_null_image(db, client):
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/create-workspace",
        headers={"Authorization": f"Bearer {access}"}, 
        data={"name": "Test Workspace"}, 
        files={},
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == "image"
    assert db.query(workspace_model.Workspace).count() == 0


# Testing /create-workspace endpoint with valid response 
def test_create_workspace_valid(db, client):
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res=db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/create-workspace",
        headers={"Authorization": f"Bearer {access}"}, 
        data={"name": "Test Workspace"}, 
        files={"image": ("test.png", BytesIO(b"fake image content"), "image/png")},
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == True
    assert db.query(workspace_model.Workspace).count() == 1 


# Testing that a workspace can be retrieved through a user
def test_method_get_workspace_by_user_id(db):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    user = repository.get_by_id(res.inserted_primary_key[0], db)

    workspace = user.workspaces[0]

    assert workspace is not None
    assert workspace.name == "Test Workspace"
    assert workspace.image == image


# Testing the delete notifications route
def test_delete_notification_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)

    user = repository.get_by_id(res.inserted_primary_key[0], db)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    n_1 = add_notification(db, "Employee Accepted Invite", f"{user.firstname} {user.surname} accepted their invite request to join your workspace.", datetime.now(), user.user_id)
    n_2 = add_notification(db, "Employee Accepted Invite", f"{user.firstname} {user.surname} accepted their invite request to join your workspace.", datetime.now(), user.user_id)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/delete-notification",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"notification_id": n_1.id}, 
    )

    response = client.send(request = req)
    assert response.status_code == 200
    remaining_notifications = db.query(workspace_model.Notification).all()
    assert db.query(workspace_model.Notification).count() == 1 
    assert remaining_notifications[0].id == n_2.id
    

# Testing the get all notifications route
def test_get_all_notifications_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)

    user = repository.get_by_id(res.inserted_primary_key[0], db)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    n_1 = add_notification(db, "Employee Accepted Invite", f"{user.firstname} {user.surname} accepted their invite request to join your workspace.", datetime.now(), user.user_id)
    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/get-notifications",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)
    data = response.json()
    assert db.query(workspace_model.Notification).count() == 1

    for n in data:
        assert data[0]["title"] == n_1.title 
        assert data[0]["body"] == n_1.body
        assert datetime.fromisoformat(n["datetime"]) == n_1.datetime
        assert data[0]["user_id"] == n_1.user_id

        

# Test the repository method to retrieve a workspace by its id 
def test_method_get_workspace_by_id(db):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_res = db.execute(workspace_insert)

    workspace = get_workspace_by_workspace_id(db, workspace_res.inserted_primary_key[0])

    assert workspace is not None


# Testing the /dashboard route with no workspace
def test_dashboard_route_without_workspace(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    res = db.execute(admin_insert)

    user = repository.get_by_id(res.inserted_primary_key[0], db)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/dashboard",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)
    data = response.json()
    for n in data:
        assert data["user"]["firstname"] == "John"
        assert data["user"]["surname"] == "Smith"
        assert data["user"]["email"] == "JohnSmith1@hotmail.com"
        assert data["user"]["role"] == "admin"
        assert data["workspace"] == None


# Testing the /dashboard route with workspace
def test_dashboard_route_with_workspace(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)

    user = repository.get_by_id(res.inserted_primary_key[0], db)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/dashboard",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)
    data = response.json()
    for n in data:
        assert data["user"]["firstname"] == "John"
        assert data["user"]["surname"] == "Smith"
        assert data["user"]["email"] == "JohnSmith1@hotmail.com"
        assert data["user"]["role"] == "employee"
        assert data["workspace"] == "Test Workspace"
        assert data["id"] == workspace_insert.inserted_primary_key[0]
        assert data["image"] == f"/workspace/image/{workspace_insert.inserted_primary_key[0]}"


# Testing the /get-workspace-image route when there is a workspace present
def test_get_workspace_image_route_with_workspace(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url=f"/workspace/image/{workspace_insert.inserted_primary_key[0]}",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200

    image_bytes = response.content 
    assert isinstance(image_bytes, bytes)


# Testing the /get-workspace-image route when there is no workspace present
def test_get_workspace_image_route_without_workspace(db, client):

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
    res = db.execute(admin_insert)
    
    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/image/1",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 404


# Test the /workspace/send-message route when a body is present
def test_successful_send_message_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", username="BobMessi1@hotmail.com", email="BobMessi1@hotmail.com", oid=oid2, refresh="ms-refresh".encode(), role="employee")

    res = db.execute(admin_insert)
    res_2 = db.execute(employee_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/send-message",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"employees":[res_2.inserted_primary_key[0]], "body":"Test Body"}
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == True

# Test the /workspace/send-message route when a body is not present
def test_invalid_send_message_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", username="BobMessi1@hotmail.com", email="BobMessi1@hotmail.com", oid=oid2, refresh="ms-refresh".encode(), role="employee")

    res = db.execute(admin_insert)
    res_2 = db.execute(employee_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/send-message",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"employees":[2], "body":None}
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == None

# Test the /workspace/get-employees route 
def test_get_all_employees_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", username="BobMessi1@hotmail.com", email="BobMessi1@hotmail.com", oid=oid2, refresh=b"ms-refresh", role="employee")
    pending_insert = insert(auth_model.PendingUser).values(email="maria@email.com", type="invite")

    res = db.execute(admin_insert)
    res_2 = db.execute(employee_insert)
    res_3 = db.execute(pending_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])
    add_pending_user_workspace(db, workspace_insert.inserted_primary_key[0], res_3.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/get-employees",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200
    response_json = response.json()  # dict
    pending_list = response_json["pending"]
    active_list = response_json["active"]

    # Check pending emails and type only
    pending_emails = [{"email": p["pending"]["email"], "type": p["pending"]["type"]} for p in pending_list]
    assert pending_emails == [{"email": "maria@email.com", "type": "invite"}]

    # Check active users
    active_user = active_list[0]["user"]
    assert active_user["email"] == "BobMessi1@hotmail.com"
    assert active_user["firstname"] == "Bob"
    assert active_user["surname"] == "Messi"
    assert active_user["role"] == "employee"

# Test the /workspace/get-workspace-roles route
def test_get_all_workspace_roles_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    res = db.execute(admin_insert)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])

    r_1 = create_role(db, "Role 1", workspace_insert.inserted_primary_key[0])
    r_2 = create_role(db, "Role 2", workspace_insert.inserted_primary_key[0])
    r_3 = create_role(db, "Role 3", workspace_insert.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/get-workspace-roles",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == [{"name":"Role 1", "role_id": r_1.role_id, "workspace_id":workspace_insert.inserted_primary_key[0]}, { "name":"Role 2", "role_id": r_2.role_id, "workspace_id":workspace_insert.inserted_primary_key[0]}, {"name":"Role 3", "role_id": r_3.role_id, "workspace_id":workspace_insert.inserted_primary_key[0]}]

# Test the delete user endpoint
def test_delete_employee_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", username="BobMessi1@hotmail.com", email="BobMessi1@hotmail.com", oid=oid2, refresh="ms-refresh".encode(), role="employee")

    res = db.execute(admin_insert)
    res_2 = db.execute(employee_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    assert db.query(auth_model.User).count() is 2

    req = client.build_request(
        method="delete",
        url=f"/workspace/delete-user/{res_2.inserted_primary_key[0]}",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert db.query(auth_model.User).count() is 1
    

# Test the reject user endpoint
def test_reject_pending_employee_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    pending_insert = insert(auth_model.PendingUser).values(email="maria@email.com", type="invite")

    res = db.execute(admin_insert)
    res_2 = db.execute(pending_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_pending_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    assert db.query(auth_model.PendingUser).count() is 1

    req = client.build_request(
        method="patch",
        url=f"/workspace/reject-pending/{res_2.inserted_primary_key[0]}",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert db.query(auth_model.PendingUser).count() is 0

# Test the /get-pending-employees route 
def test_get_pending_employees_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    pending_insert = insert(auth_model.PendingUser).values(email="mary@email.com", type="request")
    pending_insert_2 = insert(auth_model.PendingUser).values(email="joseph@email.com", type="invite")

    res = db.execute(admin_insert)
    res_2 = db.execute(pending_insert)
    res_3 = db.execute(pending_insert_2)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_pending_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])
    add_pending_user_workspace(db, workspace_insert.inserted_primary_key[0], res_3.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url=f"/workspace/get-pending-employees",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == [{'email': 'mary@email.com', 'type': 'request', 'user_id': res_2.inserted_primary_key[0]}]
    

# Test the /get-all-workspaces route
def test_get_all_workspaces(db, client):
    image = create_test_image()
    oid = "000000-7sdf77-88asdf8-9sdiy99" 

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
    res = db.execute(admin_insert)

    workspace_1 = add_workspace(db, "Workspace 1", image)
    workspace_2 = add_workspace(db, "Workspace 2", image)
    workspace_3 = add_workspace(db, "Workspace 3", image)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url=f"/workspace/get-all-workspaces",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.json() == [{"id":workspace_1.id, "name":"Workspace 1", "image":f"/workspace/image/{workspace_1.id}"}, {"id":workspace_2.id, "name":"Workspace 2", "image":f"/workspace/image/{workspace_2.id}"}, {"id":workspace_3.id, "name":"Workspace 3", "image":f"/workspace/image/{workspace_3.id}"}]
    

# Testing the request join workspace route for an expired invite
def test_request_join_workspace_route_from_expiry_error_page(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="valid@example.com", refresh="me-refresh".encode(), email="valid@example.com", oid=oid, role="admin")
    pending_user = insert(auth_model.PendingUser).values(email="valid@example.com", type="invite")

    res=db.execute(insert_statement)
    res_2=db.execute(pending_user)

    workspace = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_instance = db.execute(workspace)

    add_user_workspace(db, workspace_instance.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "employee"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url=f"/workspace/invite/request-join-workspace/{res_2.inserted_primary_key[0]}",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"title":"Test title", "body":"Test body", "workspace_id":workspace_instance.inserted_primary_key[0]},
    )
    response = client.send(request = req)

    pending = service.get_pending_by_id(db, res_2.inserted_primary_key[0])

    assert response.status_code == 200
    assert response.json() == True
    assert db.query(workspace_model.Notification).count() == 1
    assert pending.type == "request"


# Testing the request join workspace route for a user who has logged in
def test_request_join_workspace_route_from_dashboard(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf77-88asdf8-9sdiy98"

    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="valid@example.com", refresh="me-refresh".encode(), email="valid@example.com", oid=oid, role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Mark", surname="Brown", username="yes@example.com", refresh="me-refresh".encode(), email="yes@example.com", oid=oid2, role="employee")

    res=db.execute(insert_statement)
    res_2=db.execute(employee_insert)

    workspace = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_instance = db.execute(workspace)

    add_user_workspace(db, workspace_instance.inserted_primary_key[0], res.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res_2.inserted_primary_key[0], "role": "employee"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="post",
        url="/workspace/dashboard/request-join-workspace",
        headers={"Authorization": f"Bearer {access}"}, 
        json={"title":"Test title", "body":"Test body", "workspace_id":workspace_instance.inserted_primary_key[0]},
    )
    response = client.send(request = req)

    assert response.status_code == 200
    assert response.json() == True
    assert db.query(workspace_model.Notification).count() == 2
    assert db.query(workspace_model.pending_user_workspace).count() == 1
    assert db.query(auth_model.PendingUser).count() == 1
