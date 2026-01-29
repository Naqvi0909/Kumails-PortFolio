"""
Database context management for the Finance App.

This module provides a dependency injection system for database sessions,
allowing views and services to access database sessions without tight coupling.

Key Features:
- Global session factory management
- Automatic transaction handling with rollback on errors
- Context manager for safe session usage
- Thread-safe session access
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Optional


# Type alias for session factory function
SessionFactoryType = Optional[Callable[[], object]]

# Global session factory (dependency injection)
_session_factory: SessionFactoryType = None


def set_session_factory(factory: Callable[[], object]) -> None:
	"""
	Set the global session factory for dependency injection.
	
	Args:
		factory (Callable[[], object]): Function that creates database sessions
		
	Note:
		This should be called once during application startup in main.py
	"""
	global _session_factory
	_session_factory = factory


def get_session():
	"""
	Get a new database session from the factory.
	
	Returns:
		Session: SQLAlchemy database session
		
	Raises:
		RuntimeError: If session factory is not initialized
	"""
	if _session_factory is None:
		raise RuntimeError("Session factory not initialized. Call set_session_factory() first.")
	return _session_factory()


@contextmanager
def session_scope():
	"""
	Context manager for safe database session usage.
	
	Automatically handles:
	- Session creation
	- Transaction commit on success
	- Transaction rollback on errors
	- Session cleanup
	
	Usage:
		with session_scope() as session:
			# Database operations here
			pass
	
	Yields:
		Session: Database session for operations
	"""
	session = get_session()
	try:
		# Yield session for use in the context
		yield session
		# Commit transaction if no errors occurred
		session.commit()
	except Exception:
		# Rollback transaction on any error
		session.rollback()
		raise
	finally:
		# Always close the session
		session.close()


