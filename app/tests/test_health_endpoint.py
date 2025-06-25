"""Tests for the /health endpoint."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    """/health should return service status."""

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_includes_health() -> None:
    """/openapi.json should document the /health path."""

    client = TestClient(app)
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    assert "/health" in openapi.json()["paths"]


