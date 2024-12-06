from conftest import test_client

def test_register_user(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "hashed_password": "testpassword"
        },
    )
    assert response.status_code == 200
    assert "api_key" in response.json()