from app.authentication.service import create_user

# Tests to ensure that a user is added correctly when the create_user service is run
def test_create_user_service_adds_user_correctly(db):
    dummy_user = {
        "name": "John Katherine Smith",
        "email": "jkatherinesmith@outlook.com",
        "oid": "00000000-0000-0000-476j-987sdf88se" # This is random
    }

    user = create_user(db=db, details=dummy_user)

    # assertions
    assert user # Check that there is a user object returned
    assert user.firstname == "John"
    assert user.surname == "Smith"
    assert user.email == dummy_user["email"]
    assert user.oid == dummy_user["oid"]