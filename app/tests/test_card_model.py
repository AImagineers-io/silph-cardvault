"""Tests for the Card ORM model."""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.models.base import BaseModel
from app.models.card import Card


def test_card_table_created():
    """Card model should create the cards table."""
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    inspector = inspect(engine)
    assert "cards" in inspector.get_table_names()

    # Verify columns exist
    columns = {c["name"] for c in inspector.get_columns("cards")}
    expected = {
        "id",
        "set",
        "series",
        "publisher",
        "generation",
        "release_date",
        "artist",
        "name",
        "set_num",
        "types",
        "supertype",
        "subtypes",
        "level",
        "hp",
        "evolvesFrom",
        "evolvesTo",
        "abilities",
        "attacks",
        "weaknesses",
        "retreatCost",
        "convertedRetreatCost",
        "rarity",
        "flavorText",
        "nationalPokedexNumbers",
        "legalities",
        "resistances",
        "rules",
        "regulationMark",
        "ancientTrait",
    }
    assert expected.issubset(columns)

