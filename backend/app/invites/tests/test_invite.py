import pytest
import secrets

from fastapi.testclient import TestClient
from app.main import app
from app.invites.models import Invite
from app.invites.repository import add_invite, get_invite
from app.authentication.repository import add_user
from app.authentication.models import User
from app.core.database import SessionLocal, engine
from app.core.database import get_database
from datetime import datetime

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


# Test a user gets created when an invite is sent
def test_valid_invite_request_user(db_session):
    records_before = db_session.query(User).count()
    app.dependency_overrides[get_database] = lambda: db_session
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"})
    records_after = db_session.query(User).count()
    assert response.status_code == 200
    assert response.json().get("success") == True
    assert records_after == records_before + 1


# Test invite record can be retrieved using its token
def test_retrieval_invite_record(db_session):
    app.dependency_overrides[get_database] = lambda: db_session
    token = str(secrets.token_hex(16))
    user = add_user(db_session, "tomclapham21@gmail.com")
    add_invite(db_session, datetime.now(), datetime.today(), "sent", False, user.id, token)
    invite = get_invite(db_session, token)
    assert invite is not None


# Test return statement with invalid invite record which has already been used 
def test_used_invite_record(db_session):
    app.dependency_overrides[get_database] = lambda: db_session
    token = str(secrets.token_hex(16))
    user = add_user(db_session, "tomclapham21@gmail.com")
    add_invite(db_session, datetime.now(), datetime.today(), "sent", True, user.id, token)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    invite = get_invite(db_session, token)
    assert invite.used == True
    assert response.headers["location"] == "http://localhost:5173/invite-error/used"


# Test return statement with invalid invite record with invalid expiry date 
def test_expired_invite_record(db_session):
    app.dependency_overrides[get_database] = lambda: db_session
    token = str(secrets.token_hex(16))
    user = add_user(db_session, "tomclapham21@gmail.com")
    add_invite(db_session, datetime.now(), "2025-03-03", "sent", False, user.id, token)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    invite = get_invite(db_session, token)
    assert invite.status == "expired"
    assert invite.used == True
    assert response.headers["location"] == "http://localhost:5173/invite-error/expired?date=2025-03-03"


    











