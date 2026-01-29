"""
Main entry point for the Personal Finance Reconciliation Desktop App.

This module initializes the Qt application, sets up the database,
seeds it with initial data, and launches the main window.

Usage:
    python finance_app/main.py
    python -m finance_app.main
"""

from __future__ import annotations

import sys, os
# Add parent directory to path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from finance_app.db.init_db import init_db, seed_minimal
from finance_app.db.context import set_session_factory
from finance_app.views.main_window import MainWindow


def main() -> int:
	"""
	Main application entry point.
	
	Initializes the Qt application, database, and main window.
	
	Returns:
		int: Application exit code (0 for success)
	"""
	# Create Qt application instance
	app = QApplication(sys.argv)

	# Initialize database and create tables
	SessionLocal = init_db()
	# Set up session factory for dependency injection
	set_session_factory(SessionLocal)
	
	# Seed database with initial data (accounts, categories)
	session = SessionLocal()
	try:
		seed_minimal(session)
		print("✅ Database initialized with sample data")
	except Exception as e:
		print(f"⚠️  Database setup warning: {e}")
	finally:
		session.close()

	# Create and show main window
	window = MainWindow()
	window.show()
	
	# Start Qt event loop
	return app.exec()


if __name__ == "__main__":
	sys.exit(main())


