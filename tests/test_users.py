from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


def test_get_users_requires_authentication():
    response = client.get("/users/")

    assert response.status_code == 401