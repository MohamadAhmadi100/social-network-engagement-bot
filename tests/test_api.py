import pytest
from fastapi.testclient import TestClient
from main import app
from app.connection.database import Base, engine
import base64

client = TestClient(app)


def get_basic_auth_header(username="admin", password="password"):
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_profile():
    response = client.post(
        "/profiles/",
        json={"username": "testuser", "instagram_user_id": "12345"},
        headers=get_basic_auth_header()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["instagram_user_id"] == "12345"


def test_get_profile_not_found():
    response = client.get("/profiles/999", headers=get_basic_auth_header())
    assert response.status_code == 404


def test_create_alert():
    response = client.post(
        "/profiles/",
        json={"username": "testuser", "instagram_user_id": "2435234"},
        headers=get_basic_auth_header()
    )
    profile_id = response.json()["id"]
    response = client.post(
        "/alerts/",
        json={"profile_id": profile_id, "milestone": 1000},
        headers=get_basic_auth_header()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["profile_id"] == profile_id
    assert data["milestone"] == 1000
