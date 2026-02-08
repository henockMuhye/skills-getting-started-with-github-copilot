import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_and_remove_participant():
    activity = "Basketball"
    email = "testuser@mergington.edu"

    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Check participant is added
    resp_activities = client.get("/activities")
    assert email in resp_activities.json()[activity]["participants"]

    # Remove participant
    resp_remove = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp_remove.status_code == 200
    assert f"Removed {email}" in resp_remove.json()["message"]

    # Check participant is removed
    resp_activities = client.get("/activities")
    assert email not in resp_activities.json()[activity]["participants"]

def test_signup_duplicate():
    activity = "Soccer"
    email = "lucas@mergington.edu"  # already present
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]

def test_remove_nonexistent_participant():
    activity = "Art Club"
    email = "notfound@mergington.edu"
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]
