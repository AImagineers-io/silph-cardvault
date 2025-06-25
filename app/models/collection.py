"""SQLAlchemy model for user-owned card entries."""

from __future__ import annotations

from datetime import date

from sqlalchemy import String, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CollectionEntry(Base):
    """Represents a user's owned card with tracking fields."""

    __tablename__ = "collection_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    card_id: Mapped[str] = mapped_column(String(32), ForeignKey("cards.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    condition: Mapped[str | None] = mapped_column(String(30), nullable=True)
    price_paid: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    acquired_at: Mapped[date | None] = mapped_column(Date, nullable=True)

