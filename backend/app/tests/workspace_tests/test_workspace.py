from app.workspaces import models as workspace_model
from app.authentication import models as auth_model, repository, service
from app.workspaces.repository import add_user_workspace, add_notification, get_workspace_by_workspace_id
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
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
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
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="admin")
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
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", username="JohnSmith1@hotmail.com", email="JohnSmith1@hotmail.com", oid=oid, refresh="ms-refresh".encode(), role="employee")
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
        assert data["user"]["firstname"] == user.firstname
        assert data["user"]["surname"] == user.surname
        assert data["user"]["email"] == user.email
        assert data["user"]["role"] == user.role
        assert data["workspace"] == "You have not joined a workspace yet"


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
        assert data["user"]["firstname"] == user.firstname
        assert data["user"]["surname"] == user.surname
        assert data["user"]["email"] == user.email
        assert data["user"]["role"] == user.role
        assert data["workspace"] == user.workspaces[0].name


# Testing the /get-workspace-image route
def test_get_workspace_image_route(db, client):
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
        url="/workspace/get-workspace-image",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200

    image_bytes = response.content 
    assert isinstance(image_bytes, bytes)


# Test the /workspace/send-message route when a body is present
def test_successful_send_message_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    oid2 = "000000-7sdf87-88asdf8-9sdiy99"

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid, role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", email="bobmessi@hotmail.com", oid=oid2, role="employee")

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

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid, role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", email="bobmessi@hotmail.com", oid=oid2, role="employee")

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

    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid, role="admin")
    employee_insert = insert(auth_model.User).values(firstname="Bob", surname="Messi", email="bobmessi@hotmail.com", oid=oid2, role="employee")

    res = db.execute(admin_insert)
    res_2 = db.execute(employee_insert)
    
    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image)
    workspace_insert = db.execute(workspace_insert)

    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res.inserted_primary_key[0])
    add_user_workspace(db, workspace_insert.inserted_primary_key[0], res_2.inserted_primary_key[0])

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0], "role": "admin"}, refresh_family_id=refresh_family.refresh_family_id)

    req = client.build_request(
        method="get",
        url="/workspace/get-employees",
        headers={"Authorization": f"Bearer {access}"}, 
    )

    response = client.send(request = req)

    assert response.status_code == 200

# Test the /workspace/get-workspace-roles route
def test_get_all_workspace_roles_route(db, client):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid, role="admin")
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




