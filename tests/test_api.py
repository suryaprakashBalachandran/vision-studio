"""Basic tests for Vision Studio API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "Vision Studio"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models_available" in data


def test_models_endpoint():
    """Test models listing endpoint."""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Should have at least Gemini and Claude


def test_extract_missing_file():
    """Test extraction endpoint with missing file."""
    response = client.post(
        "/api/v1/extract",
        data={"ai_model": "gemini"}
    )
    assert response.status_code == 422  # Validation error


def test_extract_invalid_model():
    """Test extraction endpoint with invalid model."""
    # This would need a mock file, skipping for now
    pass


# Add more tests as needed
