import secrets
from app.invites.models import Invite
from app.invites.repository import add_invite, get_invite
from app.authentication.repository import delete_pending_user, get_pending_user_by_id
from app.authentication.models import PendingUser
from datetime import datetime, date
from sqlalchemy import insert
from urllib.parse import quote

# Test a null email input
def test_null_email_input(db, client):
    records_before = db.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":None, "expiry_date":None})
    records_after = db.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert records_after == records_before


# Test an invalid email input
def test_invalid_email_input(db, client):
    records_before = db.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":"invalid@example.com", "expiry_date":None})
    records_after = db.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "invalid"
    assert records_after == records_before


# Test a valid email input (with no expiry date selected)
def test_valid_email_input(db, client):
    records_before = db.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":None})
    records_after = db.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == "expiry"
    assert records_after == records_before


# Test a valid email with an expiry date selected
def test_valid_invite_request(db, client):
    records_before = db.query(Invite).count()
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"})
    records_after = db.query(Invite).count()
    assert response.status_code == 200
    assert response.json().get("success") == True
    assert records_after == records_before + 1


# Test a user gets created when an invite is sent
def test_valid_invite_request_user(db, client):
    records_before = db.query(PendingUser).count()
    response = client.post("/invite/send-invite", json={"email":"valid@example.com", "expiry_date":"2026-03-01T14:35:10.123456"})
    records_after = db.query(PendingUser).count()
    assert response.status_code == 200
    assert response.json().get("success") == True
    assert records_after == records_before + 1


# Test invite record can be retrieved using its token
def test_retrieval_invite_record(db):
    token = str(secrets.token_hex(16))
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com")
    res = db.execute(insert_statement)
    add_invite(db, datetime.now(), datetime.today(), False, res.inserted_primary_key[0], token)
    invite = get_invite(db, token)
    assert invite is not None


# Test return statement with invalid invite record which has already been used 
def test_used_invite_record(db, client):
    token = str(secrets.token_hex(16))
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com")
    res = db.execute(insert_statement)
    add_invite(db, datetime.now(), datetime.today(), True, res.inserted_primary_key[0], token)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    assert response.headers["location"] == "http://localhost:5173/invite-error/used"
    assert db.query(PendingUser).first() is None
    assert db.query(Invite).first() is None


# Test return statement with invalid invite record with invalid expiry date 
def test_expired_invite_record(db, client):
    token = str(secrets.token_hex(16))
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com")
    res = db.execute(insert_statement)
    add_invite(db, datetime.now(), date(2025, 3, 3), False, res.inserted_primary_key[0], token)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    assert response.headers["location"] == "http://localhost:5173/invite-error/expired?date=2025-03-03"
    assert db.query(PendingUser).first() is None
    assert db.query(Invite).first() is None 


# Test if invite is clicked when the invite is not present in database
def test_invite_clicked_when_not_in_database(db, client):
    token = str(secrets.token_hex(16))
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    assert response.headers["location"] == "http://localhost:5173/invite-error/used"


# Test return statement with valid invite
def test_valid_invite(db, client):
    token = str(secrets.token_hex(16))
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com")
    res = db.execute(insert_statement)
    add_invite(db, datetime.now(), date(2030, 3, 3), False, res.inserted_primary_key[0], token)
    response = client.get("/invite/invite-processing", params={"token": token}, follow_redirects=False)
    next_url = "/?toast=signup"
    redirect_url = f"http://localhost:8000/auth/sign-in?next={quote(next_url)}&signup=true"
    assert response.headers["location"] == redirect_url
    assert response.status_code == 302
    assert db.query(PendingUser).first() is None
    assert db.query(Invite).first() is None


# Test getting pending user by their id and deleting pending user method
def test_delete_pending_user_by_getting_id(db):
    insert_statement = insert(PendingUser).values(email="JohnSmith1@hotmail.com")
    res = db.execute(insert_statement)
    user = get_pending_user_by_id(db, res.inserted_primary_key[0])
    delete_pending_user(db, user)
    assert db.query(PendingUser).first() is None


    











