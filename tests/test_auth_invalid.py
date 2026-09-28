from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        json={
            "email": "suhana.test100@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"