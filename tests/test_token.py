from fastapi import status


def test_token_successful_login_with_registered_user(client, sample_user):
    """Test successful login with valid credentials returns token."""
    # Register user first
    client.post("/register", json=sample_user)

    # Login with form data
    login_data = {"username": sample_user["email"], "password": sample_user["password"]}
    response = client.post("/token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_token_invalid_credentials_fails(client, sample_user):
    """Test login with invalid credentials returns 401."""
    # Register user first
    client.post("/register", json=sample_user)

    # Try login with wrong password
    login_data = {"username": sample_user["email"], "password": "wrongpassword"}
    response = client.post("/token", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_token_nonexistent_user_fails(client):
    """Test login with non-existent user returns 401."""
    login_data = {"username": "nonexistent@example.com", "password": "anypassword"}
    response = client.post("/token", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"
