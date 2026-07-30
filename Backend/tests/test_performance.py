import time
import statistics
import uuid
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_01_login_response_time_under_threshold():
    email = f"perf_{uuid.uuid4().hex[:8]}@test.com"
    client.post(
        "/register",
        json={
            "name": "Perf Test",
            "email": email,
            "password": "PerfPass1",
            "role": "User",
            "date_of_birth": "1998-01-01",
        },
    )

    durations = []
    for _ in range(10):
        start = time.time()
        client.post("/login", data={"username": email, "password": "PerfPass1"})
        durations.append(time.time() - start)

    avg_time = statistics.mean(durations)
    print(f"Average login response time: {avg_time:.4f}s")
    assert avg_time < 2.0  # 2 second threshold


def test_02_concurrent_requests_home_endpoint():
    def hit_home():
        return client.get("/")

    start = time.time()
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(lambda _: hit_home(), range(50)))
    total_time = time.time() - start

    success_count = sum(1 for r in results if r.status_code == 200)
    print(f"50 concurrent requests completed in {total_time:.2f}s, {success_count}/50 succeeded")

    assert success_count == 50
    assert total_time < 10.0


def test_03_concurrent_registrations_unique_users():
    def register_user(i):
        email = f"load_{uuid.uuid4().hex[:8]}@test.com"
        return client.post(
            "/register",
            json={
                "name": f"Load User {i}",
                "email": email,
                "password": "LoadPass1",
                "role": "User",
                "date_of_birth": "1997-01-01",
            },
        )

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(register_user, range(20)))
    total_time = time.time() - start

    success_count = sum(1 for r in results if r.status_code == 200)
    print(f"20 concurrent registrations completed in {total_time:.2f}s, {success_count}/20 succeeded")

    assert success_count == 20
