def test_cannot_get_organisation_scan_endpoint(client):
    response = client.get("/scanning/organisation_scan")
    assert response.status_code == 405

