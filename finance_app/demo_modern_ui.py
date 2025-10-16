#!/usr/bin/env python
"""
Demo script to showcase the modern UI features.
Run this to see the new colorful dashboard and chart windows.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from finance_app.views.main_window import MainWindow
from finance_app.db.init_db import init_db, seed_minimal
from finance_app.db.context import set_session_factory


def main():
	"""Launch the modernized finance app."""
	app = QApplication(sys.argv)
	
	# Initialize database
	SessionLocal = init_db()
	set_session_factory(SessionLocal)
	
	# Seed with sample data
	session = SessionLocal()
	try:
		seed_minimal(session)
		print("✅ Database initialized with sample data")
	except Exception as e:
		print(f"⚠️  Database already exists: {e}")
	finally:
		session.close()
	
	# Create and show main window
	window = MainWindow()
	window.show()
	
	print("🚀 Modern Finance App launched!")
	print("📊 Features:")
	print("   • Colorful gradient dashboard")
	print("   • Modern stat cards with live data")
	print("   • Separate chart windows (click chart buttons)")
	print("   • Modern tab design with icons")
	print("   • Responsive UI with hover effects")
	
	return app.exec()


if __name__ == "__main__":
	sys.exit(main())
