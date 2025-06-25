"""SQLAlchemy model for reference Pokémon cards."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import String, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Card(Base):
    """Represents a reference Pokémon card from the PokéTCG catalogue."""

    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    set_code: Mapped[str] = mapped_column(String(20), nullable=False)
    set_name: Mapped[str] = mapped_column(String(100), nullable=False)
    number: Mapped[str] = mapped_column(String(10), nullable=False)
    supertype: Mapped[str] = mapped_column(String(50), nullable=False)
    subtypes: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    rarity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    artist: Mapped[str | None] = mapped_column(String(100), nullable=True)
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    images: Mapped[dict[str, str] | None] = mapped_column(JSON, nullable=True)
    tcgplayer_id: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)

