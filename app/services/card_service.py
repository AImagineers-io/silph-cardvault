"""Service for importing Pokémon cards from the PokéTCG API."""

from __future__ import annotations

import datetime as dt
from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card

POKETCG_API_URL = "https://api.pokemontcg.io/v2/cards"


async def fetch_card_data(card_id: str) -> dict[str, Any]:
    """Fetch raw card data from the PokéTCG API."""

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKETCG_API_URL}/{card_id}")
        response.raise_for_status()
        return response.json()["data"]


def normalize_card_data(data: dict[str, Any]) -> dict[str, Any]:
    """Map PokéTCG fields to the Card model schema."""

    release = None
    if date_str := data.get("set", {}).get("releaseDate"):
        try:
            release = dt.date.fromisoformat(date_str)
        except ValueError:
            release = dt.datetime.strptime(date_str, "%Y/%m/%d").date()

    return {
        "id": data.get("id"),
        "set": data.get("set", {}).get("id"),
        "series": data.get("set", {}).get("series"),
        "publisher": None,
        "generation": None,
        "release_date": release,
        "artist": data.get("artist"),
        "name": data.get("name"),
        "set_num": data.get("number"),
        "types": data.get("types"),
        "supertype": data.get("supertype"),
        "subtypes": data.get("subtypes"),
        "level": data.get("level"),
        "hp": data.get("hp"),
        "evolvesFrom": data.get("evolvesFrom"),
        "evolvesTo": data.get("evolvesTo"),
        "abilities": data.get("abilities"),
        "attacks": data.get("attacks"),
        "weaknesses": data.get("weaknesses"),
        "retreatCost": data.get("retreatCost"),
        "convertedRetreatCost": data.get("convertedRetreatCost"),
        "rarity": data.get("rarity"),
        "flavorText": data.get("flavorText"),
        "nationalPokedexNumbers": data.get("nationalPokedexNumbers"),
        "legalities": data.get("legalities"),
        "resistances": data.get("resistances"),
        "rules": data.get("rules"),
        "regulationMark": data.get("regulationMark"),
        "ancientTrait": data.get("ancientTrait"),
    }


async def store_card(card_data: dict[str, Any], session: AsyncSession) -> Card:
    """Insert or update a card record in the database."""

    card = await session.get(Card, card_data["id"])
    if card is None:
        card = Card(**card_data)
        session.add(card)
    else:
        for key, value in card_data.items():
            setattr(card, key, value)
    await session.commit()
    await session.refresh(card)
    return card


async def import_card(card_id: str, session: AsyncSession) -> Card:
    """Fetch a card from the PokéTCG API and persist it."""

    raw = await fetch_card_data(card_id)
    normalized = normalize_card_data(raw)
    return await store_card(normalized, session)
