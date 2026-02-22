import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.invites.models import Invite
from app.core.database import SessionLocal, engine
from app.core.database import get_database

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()  
    db = SessionLocal(bind=connection)
    yield db 
    db.close()
    transaction.rollback() 
    connection.close()

client = TestClient(app)

# Test a null email input
def test_null_email_input(db_session):
    records_before = db_session.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":None, "expiry_date":None})
    records_after = db_session.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert records_after == records_before


# Test an invalid email input
def test_invalid_email_input(db_session):
    records_before = db_session.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":"invalid@example.com", "expiry_date":None})
    records_after = db_session.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert records_after == records_before


# Test a valid email input (with no expiry date selected)
def test_valid_email_input(db_session):
    records_before = db_session.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":None})
    records_after = db_session.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "expiry"
    assert records_after == records_before


# Test a valid email with an expiry date selected
def test_valid_invite_request(db_session):
    records_before = db_session.query(Invite).count()
    app.dependency_overrides[get_database] = lambda: db_session
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"})
    records_after = db_session.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == True
    assert records_after == records_before + 1

    











