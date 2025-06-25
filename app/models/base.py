"""Base declarative class for all ORM models."""

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass

# Backwards compatible alias
Base = BaseModel

