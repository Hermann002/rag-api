import pytest
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.security.security import get_password_hash

def test_register_user(test_client: TestClient, test_db: Session):
    headers = {
        "accept": "application/json",
        "Content-type": "application/json"
    }

    response = test_client.post(
        "/auth/register",
        json={
            "username": "TestUser",
            "email": "testuser@example.com",
            "password": "testpassword"
        },
        headers=headers
    )

    data = response.json()
    assert response.status_code == 200
    assert "is_active" in response.json()
    assert data["username"] =="TestUser"
    assert "password" not in response.json()

    db_user = test_db.query(User).filter(User.email == "testuser@example.com").first()
    assert db_user is not None

def test_login_user(test_client: TestClient, test_db: Session):

    new_user = User(username="testLogin", email="loginuser@email.com", hashed_password=get_password_hash("password1"))
    test_db.add(new_user)
    test_db.commit()

    headers = {
        "accept": "application/json",
        "Content-type": "application/x-www-form-urlencoded"
    }

    response = test_client.post(
        "/auth/login",
        data={
            "username": "testLogin",
            "password": "password1"
            },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"