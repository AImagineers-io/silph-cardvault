"""SQLAlchemy model for reference Pokémon cards."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import String, Date, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Card(BaseModel):
    """Represents a reference Pokémon card aligned to the PokéTCG schema."""

    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    set: Mapped[str | None] = mapped_column(String(50), nullable=True)
    series: Mapped[str | None] = mapped_column(String(50), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(100), nullable=True)
    generation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    artist: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    set_num: Mapped[str | None] = mapped_column(String(10), nullable=True)
    types: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    supertype: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subtypes: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hp: Mapped[str | None] = mapped_column(String(10), nullable=True)
    evolvesFrom: Mapped[str | None] = mapped_column(String(100), nullable=True)
    evolvesTo: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    abilities: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    attacks: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    weaknesses: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    retreatCost: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    convertedRetreatCost: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rarity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    flavorText: Mapped[str | None] = mapped_column(String(500), nullable=True)
    nationalPokedexNumbers: Mapped[list[int] | None] = mapped_column(JSON, nullable=True)
    legalities: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    resistances: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, nullable=True)
    rules: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    regulationMark: Mapped[str | None] = mapped_column(String(10), nullable=True)
    ancientTrait: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
