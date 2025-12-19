from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "testuser@mergington.edu"

    # Clean up: try to unregister first (ignore result)
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404

    # Signup for non-existent activity
    response = client.post(f"/activities/NonExistent/signup", params={"email": email})
    assert response.status_code == 404

    # Unregister from non-existent activity
    response = client.delete(f"/activities/NonExistent/unregister", params={"email": email})
    assert response.status_code == 404
