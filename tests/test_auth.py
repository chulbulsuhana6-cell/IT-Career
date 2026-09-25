from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


def test_login_success():
    response = client.post(
        "/auth/login",
        json={
            "email": "suhana.test100@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"