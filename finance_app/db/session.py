"""
Database session management for the Finance App.

This module provides functions to create SQLAlchemy engines and session factories
for database operations. It handles SQLite database creation and connection management.

Key Functions:
- get_default_db_path(): Get the default database file path
- create_sqlite_engine(): Create SQLAlchemy engine for SQLite
- create_session_factory(): Create session factory for database operations
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Default database filename
DEFAULT_DB_FILENAME = "finance_app.db"


def get_default_db_path() -> Path:
	"""
	Get the default database file path.
	
	Returns:
		Path: Path to the default SQLite database file
	"""
	base_dir = Path.cwd()
	return base_dir / DEFAULT_DB_FILENAME


def create_sqlite_engine(db_path: Optional[Path] = None):
	"""
	Create a SQLAlchemy engine for SQLite database.
	
	Args:
		db_path (Optional[Path]): Custom database path. Uses default if None.
		
	Returns:
		Engine: SQLAlchemy engine instance
		
	Note:
		- `check_same_thread=False` allows cross-thread database access
		- `echo=False` disables SQL query logging for performance
		- `future=True` enables SQLAlchemy 2.0 features
	"""
	path = db_path or get_default_db_path()
	# `check_same_thread` disabled for potential use across threads in UI tasks
	engine = create_engine(
		f"sqlite:///{path}", 
		echo=False, 
		future=True, 
		connect_args={"check_same_thread": False}
	)
	return engine


def create_session_factory(engine):
	"""
	Create a session factory for database operations.
	
	Args:
		engine: SQLAlchemy engine instance
		
	Returns:
		sessionmaker: Configured session factory
		
	Configuration:
		- autoflush=False: Manual control over when changes are flushed
		- autocommit=False: Explicit transaction management
		- expire_on_commit=False: Objects remain accessible after commit
		- future=True: Enable SQLAlchemy 2.0 features
	"""
	return sessionmaker(
		bind=engine, 
		autoflush=False, 
		autocommit=False, 
		expire_on_commit=False, 
		future=True
	)


