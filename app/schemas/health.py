"""Pydantic schema for the health check endpoint."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Represents the service health status."""

    status: str

