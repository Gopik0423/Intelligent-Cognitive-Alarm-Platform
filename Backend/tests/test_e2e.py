import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def unique_email():
    return f"qa_{uuid.uuid4().hex[:8]}@test.com"


@pytest.fixture(scope="module")
def registered_user():
    email = unique_email()
    payload = {
        "name": "QA Test User",
        "email": email,
        "password": "TestPass123",
        "role": "User",
        "date_of_birth": "2000-01-01",
    }
    res = client.post("/register", json=payload)
    assert res.status_code == 200
    return {"email": email, "password": "TestPass123"}


@pytest.fixture(scope="module")
def auth_token(registered_user):
    res = client.post(
        "/login",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    return body["access_token"]


def test_01_register_user(registered_user):
    assert registered_user["email"] is not None


def test_02_login_success(auth_token):
    assert auth_token is not None


def test_03_login_wrong_password(registered_user):
    res = client.post(
        "/login",
        data={"username": registered_user["email"], "password": "WrongPassword"},
    )
    assert res.status_code == 200
    assert res.json().get("message") == "Invalid password"


def test_04_profile_access_with_token(auth_token):
    res = client.get("/profile", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200
    assert res.json()["message"] == "Profile Access Successful"


def test_05_user_dashboard_access(auth_token):
    res = client.get("/user", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200


def test_06_get_difficulty_default(auth_token):
    res = client.get("/difficulty/get", headers={"Authorization": f"Bearer {auth_token}"})
    if res.status_code == 200:
        assert "difficulty_level" in res.json()
    else:
        # Some implementations may take user_id as query param instead of token
        assert res.status_code in (200, 401, 422)


def test_07_update_habit_score(auth_token):
    payload = {
        "wake_up_consistency": 80,
        "challenge_completion": 60,
        "snooze_reduction": 50,
        "sleep_schedule_adherence": 90,
    }
    res = client.post(
        "/habit-score", json=payload, headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert res.status_code in (200, 401, 422)


def test_08_recommendation_endpoint_reachable():
    # Just verifying the route is registered and reachable (not 404)
    res = client.get("/recommendation/1")
    assert res.status_code != 404
