# This tests whether an unauthenticated user can access a protected endpoint
def test_unauthenticated_user_cannot_access_protected_endpoints(client):
    response = client.get("/auth/test")
    assert response.status_code == 401

# This tests whether the sign in route works without a next query parameter
def test_sign_in_without_next_query_parameter(client):
    response = client.get("/auth/sign-in")
    print(response)