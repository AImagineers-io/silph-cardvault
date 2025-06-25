"""Tests for the card import service."""

import asyncio
from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import BaseModel
from app.models.card import Card
from app.services.card_service import import_card, normalize_card_data

SAMPLE_DATA: dict[str, Any] = {
    "id": "xy1-1",
    "name": "Venusaur-EX",
    "supertype": "Pokémon",
    "subtypes": ["Basic", "EX"],
    "hp": "180",
    "types": ["Grass"],
    "evolvesTo": ["M Venusaur-EX"],
    "rules": [
        "Pokémon-EX rule: When a Pokémon-EX has been Knocked Out, your opponent takes 2 Prize cards."
    ],
    "attacks": [
        {
            "name": "Poison Powder",
            "cost": ["Grass", "Colorless", "Colorless"],
            "convertedEnergyCost": 3,
            "damage": "60",
            "text": "Your opponent's Active Pokémon is now Poisoned."
        }
    ],
    "weaknesses": [{"type": "Fire", "value": "×2"}],
    "retreatCost": ["Colorless", "Colorless", "Colorless", "Colorless"],
    "convertedRetreatCost": 4,
    "set": {"id": "xy1", "series": "XY", "releaseDate": "2014/02/05"},
    "number": "1",
    "artist": "Eske Yoshinob",
    "rarity": "Rare Holo EX",
    "nationalPokedexNumbers": [3],
    "legalities": {"unlimited": "Legal", "expanded": "Legal"},
}


def test_normalize_card_data() -> None:
    """normalize_card_data should map API fields to model columns."""

    normalized = normalize_card_data(SAMPLE_DATA)
    assert normalized["id"] == "xy1-1"
    assert normalized["name"] == "Venusaur-EX"
    assert normalized["set"] == "xy1"
    assert normalized["series"] == "XY"
    assert normalized["release_date"].isoformat() == "2014-02-05"


def test_import_card(monkeypatch) -> None:
    """import_card should fetch, normalize, and store a card."""

    async def mock_get(self, url: str) -> Any:
        class _Resp:
            def raise_for_status(self) -> None:
                return None

            def json(self) -> Any:
                return {"data": SAMPLE_DATA}

        return _Resp()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def run() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        async with async_session() as session:
            card = await import_card("xy1-1", session)
            assert card.id == "xy1-1"
            assert card.name == "Venusaur-EX"

        async with async_session() as session:
            stored = await session.get(Card, "xy1-1")
            assert stored is not None

    asyncio.run(run())

