import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]

    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg.status_code == 200
    assert f"Unregistered {email}" in response_unreg.json()["message"]

    # Try duplicate unregister
    response_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code == 400
    assert "not registered" in response_unreg2.json()["detail"]
