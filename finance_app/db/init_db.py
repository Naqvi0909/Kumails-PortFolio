"""
Database initialization and seeding for the Finance App.

This module handles database setup, table creation, and initial data seeding.
It provides functions to initialize the database schema and populate it with
essential accounts and categories.

Key Functions:
- init_db(): Initialize database and create all tables
- seed_minimal(): Add essential accounts and categories to the database
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from finance_app.db.session import create_sqlite_engine, create_session_factory
from finance_app.models.base import Base
from finance_app.models import models as m


def init_db():
	"""
	Initialize the database and create all tables.
	
	This function:
	1. Creates a SQLite engine
	2. Creates all tables defined in the models
	3. Returns a session factory for database operations
	
	Returns:
		sessionmaker: Factory for creating database sessions
	"""
	# Create SQLite engine
	engine = create_sqlite_engine()
	# Create all tables from model definitions
	Base.metadata.create_all(engine)
	# Create session factory
	SessionLocal = create_session_factory(engine)
	return SessionLocal


def seed_minimal(session: Session):
	"""
	Seed the database with essential accounts and categories.
	
	This function adds the basic chart of accounts and expense categories
	needed for the application to function properly.
	
	Args:
		session (Session): Database session for operations
		
	Note:
		This function is idempotent - it won't create duplicates if run multiple times
	"""
	# Core accounts for double-entry bookkeeping
	accounts = [
		("Checking", "asset"),      # Bank account for cash
		("Savings", "asset"),       # Savings account
		("Income", "income"),       # Income account for revenue
		("Expenses", "expense"),    # General expense account
		("Transfers", "equity"),    # Transfer account for internal transfers
	]
	
	# Create accounts if they don't exist
	for name, typ in accounts:
		if not session.query(m.Account).filter_by(name=name).first():
			session.add(m.Account(name=name, type=typ))
	
	# Example expense/income categories for transaction categorization
	categories = ["Groceries", "Rent", "Utilities", "Dining", "Salary", "Misc"]
	for name in categories:
		if not session.query(m.Category).filter_by(name=name).first():
			session.add(m.Category(name=name))

	# Commit all changes
	session.commit()


