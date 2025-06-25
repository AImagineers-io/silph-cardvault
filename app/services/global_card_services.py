import os
import httpx

from typing import Any
from dotenv import load_dotenv
from datetime import date, datetime
from app.models.card import Card
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

class GlobalCardService:
    """Service for interacting with the PokeTCG API"""

    BASE_URL = "https://api.pokemontcg.io/v2/cards"

    def __init__(self):
        self.api_key = os.getenv("PokemonTCG_Key")
        if not self.api_key:
            raise ValueError("PokemonTCG_Key not found in environment variables.")
        
        self.headers = {
            "X-API-Key": self.api_key
        }



    async def fetch_card_data(self, card_id: str) -> dict[str, Any]:
        """Fetch raw card data from the PokéTCG API by card ID.
           Single Transaction only - Can be used later in loops"""

        url = f"{self.BASE_URL}/{card_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()["data"]
        


    def normalize_card_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Normalize raw PokéTCG data to match the Card model schema."""

        release = None
        date_str = data.get("set", {}).get("releaseDate")
        if date_str:
            try:
                release = date.fromisoformat(date_str)
            except ValueError:
                try:
                    release = datetime.strptime(date_str, "%Y/%m/%d").date()
                except Exception:
                    release = None

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



    async def store_card(self, card_data: dict[str, Any], session: AsyncSession) -> Card:
        """
        Insert or update card in the local DB
        If the Card exists, update its fields.
        If not, create a new record.
        """

        existing = await session.get(Card, card_data["id"])
        if existing is None:
            new_card = Card(**card_data)
            session.add(new_card)
            await session.commit()
            await session.refresh(new_card)
            return new_card
        
        for key, value in card_data.items():
            setattr(existing, key, value)

        await session.commit()
        await session.refresh(existing)
        return existing



    async def import_card(self, card_id: str, session: AsyncSession) -> Card:
        """
        Fetch, Normalize, and Store a Single Card by ID.
        Suitable for use in single or batch import workflows
        """

        raw_data = await self.fetch_card_data(card_id)
        normalized = self.normalize_card_data(raw_data)
        return await self.store_card(normalized, session)
    
