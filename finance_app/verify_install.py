#!/usr/bin/env python
"""
Verification script to check all dependencies are installed correctly.
Run this before starting the app for the first time.
"""

import sys

def check_import(module_name, package_name=None):
    """Try to import a module and report status."""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"✓ {package_name} installed")
        return True
    except ImportError:
        print(f"✗ {package_name} NOT installed")
        return False

def main():
    print("Finance App Installation Verification")
    print("=" * 50)
    
    all_ok = True
    
    # Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"✗ Python version {version.major}.{version.minor} (need 3.10+)")
        all_ok = False
    
    print("\nChecking dependencies:")
    
    # Core dependencies
    all_ok &= check_import("PySide6", "PySide6")
    all_ok &= check_import("sqlalchemy", "SQLAlchemy")
    all_ok &= check_import("pandas", "pandas")
    all_ok &= check_import("pyqtgraph", "pyqtgraph")
    all_ok &= check_import("dateutil", "python-dateutil")
    
    # Optional
    check_import("PyInstaller", "PyInstaller (optional)")
    
    print("\nChecking project structure:")
    
    import os
    required_files = [
        "finance_app/__init__.py",
        "finance_app/main.py",
        "finance_app/db/session.py",
        "finance_app/models/models.py",
        "finance_app/views/main_window.py",
        "requirements.txt",
        "README.md"
    ]
    
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} missing")
            all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✓ All checks passed! Run: python finance_app/main.py")
        return 0
    else:
        print("✗ Some checks failed. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

