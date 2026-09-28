from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


def test_get_users_requires_authentication():
    response = client.get("/users/")

    assert response.status_code == 401


def test_user_cannot_access_another_users_account():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "suhana.test100@example.com",
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404