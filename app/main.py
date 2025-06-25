"""FastAPI application for the silph-cardvault service."""

from fastapi import FastAPI

from app.schemas import HealthResponse

from app.models.base import BaseModel
from app.db.session import engine

app = FastAPI(title="silph-cardvault")


@app.on_event("startup")
async def on_startup() -> None:
    """Create database tables on startup."""

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


@app.get("/version")
async def get_version() -> dict[str, str]:
    """Return service version metadata."""

    import json
    from pathlib import Path

    data = json.loads(Path("version.json").read_text())
    return data


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def get_health() -> HealthResponse:
    """Return basic service health status."""

    return HealthResponse(status="ok")

