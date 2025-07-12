import pytest
from fastapi import status


def test_register_successful_user_creation(client, sample_user):
    """Test successful user registration returns token."""
    response = client.post("/register", json=sample_user)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_register_duplicate_email_fails(client, sample_user):
    """Test registering with duplicate email returns error."""
    # Register user first time
    response = client.post("/register", json=sample_user)
    assert response.status_code == status.HTTP_200_OK
    
    # Try to register same email again
    response = client.post("/register", json=sample_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


def test_register_invalid_email_format_fails(client):
    """Test registration with invalid email format fails."""
    invalid_user = {
        "email": "not-an-email",
        "password": "testpassword123"
    }
    
    response = client.post("/register", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY