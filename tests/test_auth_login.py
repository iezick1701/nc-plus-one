from fastapi.testclient import TestClient
from main import app
import jwt
from db.token import get_secret, ALGORITHM

def test_check_credentials(api_client):
    response = api_client.post("/api/auth/login",json={
        "email": "user_c@example.com",
        "password": "password_c"
        }
        )
    assert response.status_code == 200
    assert "token" in response.json()

def test_incorrect_cred(api_client):
    response = api_client.post("/api/auth/login",json={
            "email": "fdsffew",
            "password": "password_c"
            }
            )
    assert response.status_code == 401


def test_missing_cred(api_client):
    response = api_client.post("/api/auth/login",json={
            "email": "user_c@example.com"
            }
            )
    assert response.status_code == 400

def test_check_token(api_client):
    response = api_client.post("/api/auth/login",json={
            "email": "user_c@example.com",
            "password": "password_c"
            }
            )
    user = jwt.decode(response.json()["token"],get_secret(),algorithms=[ALGORITHM])
    assert (user["sub"]) == "1"
    

    