from app.workspaces import models as workspace_model
from app.workspaces.repository import get_workspace_by_user_id
from app.authentication import models as auth_model, repository, service
from sqlalchemy import insert, select, desc

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
    admin = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res=db.execute(admin)

    workspace = insert(workspace_model.Workspace).values(name="Test Workspace", image=image, user_id=res.inserted_primary_key[0])
    db.execute(workspace)

    assert db.query(workspace_model.Workspace).count() == 1 

# Testing /create-workspace endpoint with null name
def test_create_workspace_null_name(db, client):
    oid = "000000-7sdf77-88asdf8-9sdiy99"
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

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
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res=db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

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
    insert_statement = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res=db.execute(insert_statement)

    refresh_family = repository.create_refresh_family(db)

    access, refresh, _ = service.create_access_refresh(db, data={"userId": res.inserted_primary_key[0]}, refresh_family_id=refresh_family.refresh_family_id)

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

# Testing that a workspace can be retrieved with a user's id
def test_method_get_workspace_by_user_id(db):
    image = create_test_image()

    oid = "000000-7sdf77-88asdf8-9sdiy99"
    admin_insert = insert(auth_model.User).values(firstname="John", surname="Smith", email="JohnSmith1@hotmail.com", oid=oid)
    res = db.execute(admin_insert)

    workspace_insert = insert(workspace_model.Workspace).values(name="Test Workspace", image=image, user_id=res.inserted_primary_key[0])
    db.execute(workspace_insert)

    workspace = get_workspace_by_user_id(db, res.inserted_primary_key[0])

    assert workspace is not None
    assert workspace.name == "Test Workspace"
    assert workspace.image == image



