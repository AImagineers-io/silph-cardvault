"""Tests for the Card ORM model."""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.card import Card


def test_card_table_created():
    """Card model should create the cards table."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    assert "cards" in inspector.get_table_names()

    # Verify columns exist
    columns = {c["name"] for c in inspector.get_columns("cards")}
    expected = {"id", "name", "set_code", "set_name", "number", "supertype", "subtypes", "rarity", "artist", "release_date", "images", "tcgplayer_id"}
    assert expected.issubset(columns)

