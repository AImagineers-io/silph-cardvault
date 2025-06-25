"""Tests for the CollectionEntry ORM model."""

from sqlalchemy import create_engine, inspect

from app.models.base import BaseModel
from app.models.collection import CollectionEntry


def test_collection_entry_table_created() -> None:
    """CollectionEntry model should create the collection_entries table."""
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    inspector = inspect(engine)
    assert "collection_entries" in inspector.get_table_names()

    columns = {c["name"] for c in inspector.get_columns("collection_entries")}
    expected = {
        "id",
        "user_id",
        "card_id",
        "quantity",
        "condition",
        "price_paid",
        "acquired_at",
    }
    assert expected.issubset(columns)
