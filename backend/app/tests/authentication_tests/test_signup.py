from app.authentication.service import create_user
from app.tests.authentication_tests.dummy_user import User

dummy_user = User()

# Tests to ensure that a user is added correctly when the create_user service is run
def test_create_user_service_adds_user_correctly(db):
    details = {
        "name": "John Katherine Smith",
        "email": dummy_user.email,
        "preferred_username": dummy_user.username,
        "oid": dummy_user.oid
    }

    user = create_user(db=db, details=details, refresh="test_refresh")
    print(user)

    # assertions
    assert user # Check that there is a user object returned
    assert user.firstname == "John"
    assert user.surname == "Smith"
    assert user.email == dummy_user.email
    assert user.oid == dummy_user.oid