from app.workspaces import service, models
from sqlalchemy import insert
from io import BytesIO
from PIL import Image
import base64

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
    insert_statement = insert(models.Workspace).values(name="Test Workspace", image=image)
    db.execute(insert_statement)
    assert db.query(models.Workspace).count() == 1 

# Testing /create-workspace endpoint with null name
def test_create_workspace_null_name(db, client):
    response = client.post("/workspace/create-workspace", json={"name":None, "image":None})
    assert response.status_code == 200
    assert response.json() == "name"
    assert db.query(models.Workspace).count() == 0 


# Testing /create-workspace endpoint with null image
def test_create_workspace_null_image(db, client):
    response = client.post("/workspace/create-workspace", json={"name":"Test Workspace", "image":None})
    assert response.status_code == 200
    assert response.json() == "image"
    assert db.query(models.Workspace).count() == 0


# Testing /create-workspace endpoint with valid response 
def test_create_workspace_valid(db, client):
    image = create_test_image()
    encoded_image = base64.b64encode(image).decode()
    response = client.post("/workspace/create-workspace", json={"name":"Test Workspace", "image":encoded_image})
    assert response.status_code == 200
    assert response.json() == True
    assert db.query(models.Workspace).count() == 1 