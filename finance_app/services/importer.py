"""
CSV import service for bank statement processing.

This module handles importing CSV bank statements with flexible column mapping,
date parsing, and transaction creation. It supports multiple date formats and
automatically creates accounts if they don't exist.

Key Functions:
- ImportMapping: Data class for column mapping configuration
- parse_date(): Parse dates in multiple formats
- preview_dataframe(): Preview CSV data before import
- import_transactions(): Import transactions from CSV to database
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import pandas as pd

from finance_app.models import models as m


# Supported date formats for parsing bank statement dates
SUPPORTED_DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y"]


@dataclass
class ImportMapping:
	"""
	Configuration for CSV column mapping during import.
	
	This class defines which CSV columns map to which transaction fields,
	allowing flexible import from different bank statement formats.
	
	Attributes:
		date_col (str): CSV column name containing transaction dates
		description_col (str): CSV column name containing transaction descriptions
		amount_col (str): CSV column name containing transaction amounts
		source_account_name (str): Account name to assign transactions to
	"""
	date_col: str
	description_col: str
	amount_col: str
	source_account_name: str


def parse_date(value: str) -> datetime.date:
	"""
	Parse a date string using supported formats.
	
	Attempts to parse the date using common bank statement formats.
	Supports both ISO format (YYYY-MM-DD) and US format (MM/DD/YYYY).
	
	Args:
		value (str): Date string to parse
		
	Returns:
		datetime.date: Parsed date object
		
	Raises:
		ValueError: If date format is not recognized
	"""
	# Try each supported format until one works
	for fmt in SUPPORTED_DATE_FORMATS:
		try:
			return datetime.strptime(str(value).strip(), fmt).date()
		except Exception:
			continue
	# If no format matches, raise an error
	raise ValueError(f"Unrecognized date format: {value}")


def preview_dataframe(path: str, n: int = 50) -> pd.DataFrame:
	"""
	Preview CSV data before importing.
	
	Loads the first N rows of a CSV file to show the user what data
	will be imported, allowing them to verify column mapping.
	
	Args:
		path (str): Path to CSV file
		n (int): Number of rows to preview (default: 50)
		
	Returns:
		pd.DataFrame: First N rows of the CSV file
	"""
	df = pd.read_csv(path, nrows=n)
	return df


def import_transactions(session, csv_path: str, mapping: ImportMapping) -> int:
	"""
	Import transactions from CSV file to database.
	
	Reads a CSV file and creates Transaction records based on the column mapping.
	Automatically creates the source account if it doesn't exist.
	Skips rows with invalid dates or amounts.
	
	Args:
		session: Database session for operations
		csv_path (str): Path to CSV file to import
		mapping (ImportMapping): Column mapping configuration
		
	Returns:
		int: Number of transactions successfully imported
		
	Note:
		This function is idempotent - running it multiple times with the same
		data will create duplicate transactions. Use with caution.
	"""
	# Load CSV file into pandas DataFrame
	df = pd.read_csv(csv_path)

	# Ensure source account exists, create if necessary
	account = session.query(m.Account).filter_by(name=mapping.source_account_name).first()
	if account is None:
		# Create new account as asset type (bank account)
		account = m.Account(name=mapping.source_account_name, type="asset")
		session.add(account)
		session.flush()  # Flush to get the ID

	created = 0
	# Process each row in the CSV
	for _, row in df.iterrows():
		try:
			# Parse date, skip row if invalid
			dt = parse_date(row[mapping.date_col])
		except Exception:
			# Skip rows with invalid dates
			continue
		
		# Extract transaction data
		desc = str(row[mapping.description_col])
		amt = float(row[mapping.amount_col])

		# Create transaction record
		txn = m.Transaction(
			date=dt,
			description=desc,
			amount=amt,
			source_account_id=account.id,
		)
		session.add(txn)
		created += 1

	return created


