"""
Base model classes for the Finance App database models.

This module defines the base classes for all database models, providing
common functionality like primary keys and inheritance structure.

Classes:
- Base: SQLAlchemy declarative base for all models
- IdentifiedBase: Abstract base with auto-incrementing ID field
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer


class Base(DeclarativeBase):
	"""
	SQLAlchemy declarative base for all database models.
	
	This is the base class that all database models inherit from.
	It provides the foundation for SQLAlchemy's declarative mapping.
	"""
	pass


class IdentifiedBase(Base):
	"""
	Abstract base class for models with auto-incrementing ID.
	
	This class provides a common ID field for all models that need
	a primary key. It's marked as abstract so it won't create a table.
	
	Attributes:
		id (int): Auto-incrementing primary key
	"""
	__abstract__ = True

	# Auto-incrementing primary key field
	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


