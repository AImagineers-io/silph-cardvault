import os
import httpx

from typing import Any
from dotenv import load_dotenv

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