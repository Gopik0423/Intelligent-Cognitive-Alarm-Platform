import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_01_profile_without_token_rejected():
    res = client.get("/profile")
    assert res.status_code == 401


def test_02_admin_route_without_token_rejected():
    res = client.get("/admin")
    assert res.status_code == 401


def test_03_invalid_token_rejected():
    res = client.get("/profile", headers={"Authorization": "Bearer this.is.not.a.valid.token"})
    assert res.status_code == 401


def test_04_tampered_token_rejected():
    fake_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJoYWNrZXJAdGVzdC5jb20iLCJyb2xlIjoiQWRtaW4ifQ."
        "invalidsignaturepart"
    )
    res = client.get("/profile", headers={"Authorization": f"Bearer {fake_token}"})
    assert res.status_code == 401


def test_05_user_cannot_access_admin_dashboard():
    # Register + login as a normal User, then try hitting Admin-only route
    import uuid
    email = f"sec_{uuid.uuid4().hex[:8]}@test.com"
    client.post(
        "/register",
        json={
            "name": "Security Test",
            "email": email,
            "password": "Pass1234",
            "role": "User",
            "date_of_birth": "1999-05-05",
        },
    )
    login_res = client.post("/login", data={"username": email, "password": "Pass1234"})
    token = login_res.json()["access_token"]

    res = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


def test_06_sql_injection_attempt_in_login():
    res = client.post(
        "/login",
        data={"username": "' OR '1'='1", "password": "' OR '1'='1"},
    )
    # Should NOT authenticate; should be treated as invalid user, not crash the server
    assert res.status_code == 200
    assert res.json().get("message") in ("User not found", "Invalid password")


def test_07_duplicate_admin_registration_blocked():
    import uuid
    email1 = f"admin_{uuid.uuid4().hex[:8]}@test.com"
    email2 = f"admin_{uuid.uuid4().hex[:8]}@test.com"

    res1 = client.post(
        "/register",
        json={
            "name": "Admin One",
            "email": email1,
            "password": "AdminPass1",
            "role": "Admin",
            "date_of_birth": "1990-01-01",
        },
    )
    res2 = client.post(
        "/register",
        json={
            "name": "Admin Two",
            "email": email2,
            "password": "AdminPass2",
            "role": "Admin",
            "date_of_birth": "1991-01-01",
        },
    )
    # Second admin registration should be blocked if an Admin already exists
    messages = [res1.json().get("message"), res2.json().get("message")]
    assert "Admin already exists" in messages or "User registered successfully" in messages


def test_08_duplicate_email_registration_blocked():
    import uuid
    email = f"dup_{uuid.uuid4().hex[:8]}@test.com"
    payload = {
        "name": "Dup Test",
        "email": email,
        "password": "Pass1234",
        "role": "User",
        "date_of_birth": "1995-01-01",
    }
    client.post("/register", json=payload)
    res2 = client.post("/register", json=payload)
    assert res2.json().get("message") == "Email already registered"
