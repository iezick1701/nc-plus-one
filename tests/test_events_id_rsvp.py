from fastapi.testclient import TestClient
from main import app

def test_create_rsvp(api_client):
    login_response = api_client.post("/api/auth/login",json={
        "email": "user_c@example.com",
        "password": "password_c"
        }
        )
    auth_token = login_response.json()["token"]
    response = api_client.post("/api/events/2/rsvp",headers={
        "Authorization": f"Bearer {auth_token}"
        }
        )
    assert response.status_code == 201
    