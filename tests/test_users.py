from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


def test_get_users_requires_authentication():
    response = client.get("/users/")

    assert response.status_code == 401


def test_user_cannot_access_another_existing_user():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "suhana.test100@example.com",
            "password": "TestPassword123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    users_response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert users_response.status_code == 200

    second_user = next(
        user
        for user in users_response.json()
        if user["email"] == "ownership.test@example.com"
    )

    response = client.get(
        f"/users/{second_user['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only access your own account"