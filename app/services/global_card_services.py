import os
import httpx

from typing import Any
from dotenv import load_dotenv
from datetime import date, datetime
from app.models.card import Card
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
    


    async def fetch_all_remote_card_ids(self) -> list[str]:
        """
        Fetch all Pokemon Card IDs from PokeTCG.io using pagination
        Returns a list of card IDs
        """
        all_ids = []
        page = 1
        page_size = 250

        async with httpx.AsyncClient() as client:
            while True:
                url = f"{self.BASE_URL}?page={page}&pageSize={page_size}"
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()

                data = response.json()["data"]
                if not data:
                    break
                
                ids = [card["id"] for card in data]
                all_ids.extend(ids)

                page += 1
        
        return all_ids
    
    async def get_all_local_cards_ids(self, session: AsyncSession) -> set[str]:
        """
        Fetch all cards IDS currently stored in the local database.
        Returns a set of card IDs
        """
        result = await session.execute(
            select(Card.id)
        )
        rows = result.scalars().all()
        return set(rows)
    
    async def sync_missing_cards(self, session: AsyncSession) -> int:
        """"
        Fetch missing card IDs and import only those not yet in local DB
        Return the number of cards imported.
        """
        remote_ids = set(await self.fetch_all_remote_card_ids())
        local_ids = await self.get_all_local_cards_ids(session)
        missing_ids = remote_ids - local_ids

        print(f"[SYNC] Missing cards to import: {len(missing_ids)}")

        imported = 0
        for card_id in missing_ids:
            try:
                await self.import_card(card_id, session)
                imported += 1
            except Exception as e:
                print(f"[ERROR] Failed to import card {card_id}: {e}")
        
        print(f"[SYNC COMPLETE] Imported {imported} new cards.")
        return imported