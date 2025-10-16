"""
Database models for the Personal Finance Reconciliation App.

This module defines all the SQLAlchemy ORM models that represent the database schema.
The models implement a double-entry bookkeeping system with transaction categorization.

Key Models:
- Account: Chart of accounts (assets, liabilities, income, expenses, equity)
- Transaction: Financial transactions from bank statements
- Posting: Double-entry bookkeeping entries (debits and credits)
- Category: Transaction categories for expense/income classification
- Rule: Automated categorization rules using regex patterns
- PeriodClosure: Month-end reconciliation locks

Database Design:
The schema follows double-entry bookkeeping principles where every transaction
creates balanced postings (total debits = total credits).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Date, DateTime, Numeric, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import IdentifiedBase


class Account(IdentifiedBase):
	"""
	Chart of accounts for double-entry bookkeeping.
	
	Represents different types of accounts in the accounting system:
	- Assets: Cash, bank accounts, investments
	- Liabilities: Debts, loans, credit cards
	- Income: Revenue, salary, interest
	- Expenses: Costs, bills, purchases
	- Equity: Net worth, retained earnings
	
	Attributes:
		name (str): Account name (e.g., "Checking", "Salary")
		type (str): Account type (asset, liability, income, expense, equity)
		postings (list[Posting]): All postings (debits/credits) for this account
	"""
	__tablename__ = "accounts"

	# Account name - must be unique
	name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
	# Account type for double-entry bookkeeping
	type: Mapped[str] = mapped_column(String(32), nullable=False)  # e.g., asset, liability, income, expense, equity

	# Relationship to all postings for this account
	postings: Mapped[list["Posting"]] = relationship(back_populates="account")


class Category(IdentifiedBase):
	"""
	Transaction categories for expense/income classification.
	
	Used to categorize transactions for reporting and analysis.
	Supports hierarchical categories with parent-child relationships.
	
	Attributes:
		name (str): Category name (e.g., "Groceries", "Rent")
		parent_id (Optional[int]): Parent category ID for hierarchy
		parent (Optional[Category]): Parent category relationship
		transactions (list[Transaction]): All transactions in this category
	"""
	__tablename__ = "categories"

	# Category name - must be unique
	name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
	# Parent category for hierarchical organization
	parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

	# Self-referential relationship for category hierarchy
	parent: Mapped[Optional["Category"]] = relationship(remote_side="Category.id")
	# All transactions categorized under this category
	transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")


class Transaction(IdentifiedBase):
	"""
	Financial transactions imported from bank statements.
	
	Represents individual financial transactions with amounts, dates, and descriptions.
	Each transaction can be categorized and will generate double-entry postings.
	
	Attributes:
		date (date): Transaction date
		description (str): Transaction description from bank statement
		amount (float): Transaction amount (positive for income, negative for expenses)
		source_account_id (int): Bank account where transaction occurred
		normalized_memo (Optional[str]): Cleaned/standardized description
		category_id (Optional[int]): Assigned category for this transaction
		source_account (Account): Bank account relationship
		category (Optional[Category]): Assigned category relationship
		postings (list[Posting]): Double-entry postings for this transaction
	"""
	__tablename__ = "transactions"

	# Transaction date
	date: Mapped[date] = mapped_column(Date, nullable=False)
	# Original description from bank statement
	description: Mapped[str] = mapped_column(String(255), nullable=False)
	# Transaction amount (positive = income, negative = expense)
	amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
	# Bank account where transaction occurred
	source_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
	# Cleaned/standardized description for better matching
	normalized_memo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
	# Assigned category (None if uncategorized)
	category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

	# Relationships
	source_account: Mapped["Account"] = relationship()
	category: Mapped[Optional["Category"]] = relationship(back_populates="transactions")
	# Double-entry postings for this transaction
	postings: Mapped[list["Posting"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")


class Posting(IdentifiedBase):
	"""
	Double-entry bookkeeping entries for transactions.
	
	Each transaction creates two postings that must balance (total debits = total credits).
	This ensures the accounting equation remains balanced: Assets = Liabilities + Equity.
	
	Attributes:
		transaction_id (int): Associated transaction
		account_id (int): Account being debited or credited
		debit (float): Debit amount (must be >= 0)
		credit (float): Credit amount (must be >= 0)
		transaction (Transaction): Associated transaction relationship
		account (Account): Account being posted to
		
	Constraints:
		- Both debit and credit must be non-negative
		- At least one of debit or credit must be > 0
		- Total debits must equal total credits for each transaction
	"""
	__tablename__ = "postings"

	# Associated transaction
	transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), nullable=False, index=True)
	# Account being debited or credited
	account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
	# Debit amount (increases assets/expenses, decreases liabilities/income)
	debit: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
	# Credit amount (decreases assets/expenses, increases liabilities/income)
	credit: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)

	# Relationships
	transaction: Mapped["Transaction"] = relationship(back_populates="postings")
	account: Mapped["Account"] = relationship(back_populates="postings")

	# Database constraints
	__table_args__ = (
		# Ensure both debit and credit are non-negative
		CheckConstraint("(debit >= 0) AND (credit >= 0)", name="ck_postings_non_negative"),
	)


class Rule(IdentifiedBase):
	"""
	Automated categorization rules for transactions.
	
	Rules use regex patterns to automatically categorize transactions based on
	description text and optional amount ranges. Rules are evaluated in priority order.
	
	Attributes:
		pattern (str): Regex pattern to match transaction descriptions
		category_id (int): Category to assign when pattern matches
		amount_min (Optional[float]): Minimum amount for rule to apply
		amount_max (Optional[float]): Maximum amount for rule to apply
		priority (int): Rule evaluation order (lower = higher priority)
		active (bool): Whether rule is currently active
		category (Category): Assigned category relationship
		
	Example:
		pattern="grocery|walmart|target" matches grocery store transactions
		amount_min=10.0, amount_max=100.0 matches transactions between $10-$100
	"""
	__tablename__ = "rules"

	# Regex pattern to match transaction descriptions
	pattern: Mapped[str] = mapped_column(String(255), nullable=False)
	# Category to assign when pattern matches
	category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
	# Optional minimum amount filter
	amount_min: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
	# Optional maximum amount filter
	amount_max: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
	# Rule priority (lower number = higher priority)
	priority: Mapped[int] = mapped_column(nullable=False, default=100)
	# Whether rule is currently active
	active: Mapped[bool] = mapped_column(nullable=False, default=True)

	# Relationship to assigned category
	category: Mapped["Category"] = relationship()


class PeriodClosure(IdentifiedBase):
	"""
	Month-end reconciliation locks to prevent editing closed periods.
	
	Once a period is closed, transactions in that period cannot be modified
	to maintain data integrity and audit trails.
	
	Attributes:
		period_start (date): Start date of the closed period
		period_end (date): End date of the closed period
		closed_at (datetime): When the period was closed
		
	Constraints:
		- Only one closure per period (unique constraint on start/end dates)
	"""
	__tablename__ = "period_closures"

	# Start date of the closed period
	period_start: Mapped[date] = mapped_column(Date, nullable=False)
	# End date of the closed period
	period_end: Mapped[date] = mapped_column(Date, nullable=False)
	# Timestamp when period was closed
	closed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	# Database constraints
	__table_args__ = (
		# Ensure only one closure per period
		UniqueConstraint("period_start", "period_end", name="uq_period"),
	)


