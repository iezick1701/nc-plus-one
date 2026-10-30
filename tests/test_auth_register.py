from fastapi.testclient import TestClient
from main import app
from db.password import check_pwd
from db.connection import get_connection


def test_password_not_in_response(api_client):
    response = api_client.post("/api/auth/register",json={
        "email": "user_d@example.com",
        "password": "password_c",
        "name": "user_c"
        })

    assert "password" not in response.json()["user"]
    assert response.status_code == 201

def test_successful_registrations(api_client):
    response = api_client.post("/api/auth/register",json={
        "email": "user_d@example.com",
        "password": "password_c",
        "name": "user_c"
        })

    assert response.status_code == 201
    assert "id"and"created_at" in response.json()["user"]
    assert response.json()["user"]["email"] == "user_d@example.com"
    assert response.json()["user"]["name"] == "user_c"

def test_password_is_hashed(api_client):
    response = api_client.post("/api/auth/register", json={
        "email": "user_d@example.com",
        "password": "password_d",
        "name": "user_d"
    })

    assert response.status_code == 201

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT password FROM users WHERE email = %s",
                ("user_d@example.com",)
            )
            stored_hash = cursor.fetchone()[0]

    assert check_pwd("password_d", stored_hash)
    

def test_status_code_for_duplicate_emails(api_client):
    response = api_client.post("/api/auth/register",json={
        "email": "user_c@example.com",
        "password": "password_c",
        "name": "user_c"
        })

    assert response.status_code == 409

def test_status_code_missing_fields(api_client):
    response = api_client.post("/api/auth/register",json={
        "email": "user_c@example.com",
        "password": "password_c",
        })

    assert response.status_code == 400
    