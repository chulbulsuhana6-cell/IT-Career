from fastapi.testclient import TestClient

from python.main import app


client = TestClient(app)


TEST_EMAIL = "suhana.test100@example.com"
TEST_PASSWORD = "TestPassword123"


def get_token():
    response = client.post(
        "/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_get_jobs_requires_authentication():
    response = client.get("/jobs/")

    assert response.status_code == 401


def test_create_job():
    token = get_token()

    response = client.post(
        "/jobs/",
        json={
            "company": "Microsoft",
            "role": "Backend Developer",
            "location": "Hyderabad",
            "status": "Applied"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Microsoft"
    assert data["role"] == "Backend Developer"
    assert data["status"] == "Applied"
    assert "id" in data


def test_get_jobs_authenticated():
    token = get_token()

    response = client.get(
        "/jobs/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_and_delete_job():
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_response = client.post(
        "/jobs/",
        json={
            "company": "Amazon",
            "role": "Python Developer",
            "location": "Pune",
            "status": "Applied"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["id"]

    update_response = client.put(
        f"/jobs/{job_id}",
        json={
            "company": "Amazon",
            "role": "Backend Software Engineer",
            "location": "Pune",
            "status": "Interview"
        },
        headers=headers
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Interview"

    delete_response = client.delete(
        f"/jobs/{job_id}",
        headers=headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Job deleted successfully"


def test_job_ownership():
    token = get_token()

    create_response = client.post(
        "/jobs/",
        json={
            "company": "Ownership Test Company",
            "role": "Backend Developer",
            "location": "Pune",
            "status": "Applied"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["id"]

    second_user_login = client.post(
        "/auth/login",
        json={
            "email": "ownership.test@example.com",
            "password": "TestPassword123"
        }
    )

    assert second_user_login.status_code == 200

    second_token = second_user_login.json()["access_token"]

    response = client.get(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {second_token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You can only access your own jobs"

    cleanup_response = client.delete(
        f"/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert cleanup_response.status_code == 200