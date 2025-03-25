import pytest
import requests
from main import get_api_key, get_coordinates, BASE_URL, API_KEY

# Test if the API key is correctly loaded
def test_api_key_present():
    """Ensure API key is loaded from the file."""
    api_key = get_api_key()
    assert api_key is not None and len(api_key) > 0


# Test if valid locations return correct coordinates
def test_valid_location():
    """Check if the function returns coordinates for valid locations."""
    coordinates = get_coordinates("Cumbria")
    assert coordinates == (54.4609, -3.0886)


# Test if the API call succeeds with valid coordinates
def test_successful_api_call():
    """VVerify that the API returns data for a valid request."""
    lat, lon = 54.4609, -3.0886  # Cumbria
    response = requests.get(f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    assert response.status_code == 200  # Should return OK status
    data = response.json()
    assert "main" in data and "temp" in data["main"]  # Check for temperature data


# Test if an invalid API key returns 401 Unauthorized
def test_invalid_api_key():
    """Ensure the API responds with 401 for an invalid API key."""
    lat, lon = 54.4609, -3.0886
    fake_api_key = "invalid_api_key"
    response = requests.get(f"{BASE_URL}?lat={lat}&lon={lon}&appid={fake_api_key}&units=metric")
    assert response.status_code == 401  # Unauthorized


# Test if an invalid location triggers an error
def test_invalid_location():
    """Ensure invalid locations are handled properly"""
    coordinates = get_coordinates("InvalidLocation")
    assert coordinates is None  # Should return None for an invalid location
