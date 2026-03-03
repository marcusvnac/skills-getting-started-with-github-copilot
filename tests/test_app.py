from fastapi.testclient import TestClient
import pytest

from src.app import app

@pytest.fixture

def client():
    # Arrange: create a fresh test client for each test
    return TestClient(app)


def test_get_activities(client):
    # Arrange: client fixture gives us a client

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    # the initial dataset defined in src/app.py should include Chess Club
    assert "Chess Club" in data


def test_signup_and_prevent_duplicates(client):
    # Arrange
    activity = "Chess Club"
    email = "test@school.edu"

    # Act - first signup should succeed
    r1 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert r1.status_code == 200
    assert "Signed up" in r1.json()["message"]

    # Act - same email signup again should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert r2.status_code == 400


def test_unsubscribe_and_edge_cases(client):
    # Arrange
    activity = "Chess Club"
    email = "remove@school.edu"

    # sign up first to ensure the participant exists
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act - unsubscribe success
    ru = client.post(f"/activities/{activity}/unsubscribe?email={email}")
    # Assert
    assert ru.status_code == 200
    assert "Unregistered" in ru.json()["message"]

    # Act - unsubscribing again should give 400
    ru2 = client.post(f"/activities/{activity}/unsubscribe?email={email}")
    assert ru2.status_code == 400

    # Act - signup/unsubscribe for nonexistent activity
    r404 = client.post(f"/activities/unknown/signup?email=foo@x.com")
    assert r404.status_code == 404
    r404u = client.post(f"/activities/unknown/unsubscribe?email=foo@x.com")
    assert r404u.status_code == 404
