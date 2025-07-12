import pytest
from fastapi import status


def test_me_with_valid_token_returns_user_info(client, sample_user):
    """Test /me endpoint with valid token returns user information."""
    # Register and get token
    response = client.post("/register", json=sample_user)
    token = response.json()["access_token"]
    
    # Access /me endpoint with token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == sample_user["email"]


def test_me_with_invalid_token_fails(client):
    """Test /me endpoint with invalid token returns 401."""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/me", headers=headers)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"


def test_me_without_token_fails(client):
    """Test /me endpoint without authentication returns 401."""
    response = client.get("/me")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED