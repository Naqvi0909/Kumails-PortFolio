"""
Double-entry posting generator for the Finance App.

This module implements the core double-entry bookkeeping logic, automatically
generating balanced debit/credit postings for each transaction. This ensures
the fundamental accounting equation remains balanced: Assets = Liabilities + Equity.

Key Features:
- Automatic posting generation for income and expense transactions
- Balanced double-entry bookkeeping (total debits = total credits)
- Dynamic account creation based on transaction categories
- Batch processing for performance

Key Functions:
- generate_postings_for_transaction(): Create postings for a single transaction
- generate_all_postings(): Create postings for all uncategorized transactions

Double-Entry Rules:
- Expenses: Credit source account (money out), Debit expense account
- Income: Debit source account (money in), Credit income account
- Each transaction creates exactly 2 postings that must balance
"""

from __future__ import annotations

from typing import Optional

from finance_app.models import models as m


def generate_postings_for_transaction(session, transaction: m.Transaction) -> int:
	"""
	Generate double-entry postings for a single transaction.
	
	Creates balanced debit/credit postings according to double-entry bookkeeping
	principles. Each transaction generates exactly 2 postings that must balance.
	
	Args:
		session: Database session for operations
		transaction (Transaction): Transaction to generate postings for
		
	Returns:
		int: Number of postings created (always 2)
		
	Posting Logic:
		For Expenses (amount < 0):
			- Credit source account (money out of bank)
			- Debit expense account (increase expense)
			
		For Income (amount > 0):
			- Debit source account (money into bank)
			- Credit income account (increase income)
			
	Note:
		This function clears any existing postings for the transaction before
		creating new ones, ensuring no duplicate postings.
	"""
	# Clear any existing postings for this transaction
	session.query(m.Posting).filter(m.Posting.transaction_id == transaction.id).delete()
	
	# Determine if this is an expense or income based on amount sign
	if transaction.amount < 0:
		# EXPENSE TRANSACTION (money going out)
		# Get or create expense account
		if transaction.category_id:
			# Use category-specific expense account
			category = session.get(m.Category, transaction.category_id)
			expense_account = session.query(m.Account).filter_by(name=f"Expense:{category.name}").first()
			if not expense_account:
				# Create new category-specific expense account
				expense_account = m.Account(name=f"Expense:{category.name}", type="expense")
				session.add(expense_account)
				session.flush()  # Flush to get the ID
		else:
			# Use general expense account for uncategorized transactions
			expense_account = session.query(m.Account).filter_by(name="Expenses").first()
		
		# Create balanced postings for expense
		# Posting 1: Credit source account (money out of bank)
		posting1 = m.Posting(
			transaction_id=transaction.id,
			account_id=transaction.source_account_id,
			debit=0,
			credit=abs(transaction.amount)  # Credit the bank account
		)
		# Posting 2: Debit expense account (increase expense)
		posting2 = m.Posting(
			transaction_id=transaction.id,
			account_id=expense_account.id,
			debit=abs(transaction.amount),  # Debit the expense account
			credit=0
		)
	else:
		# INCOME TRANSACTION (money coming in)
		# Get or create income account
		if transaction.category_id:
			# Use category-specific income account
			category = session.get(m.Category, transaction.category_id)
			income_account = session.query(m.Account).filter_by(name=f"Income:{category.name}").first()
			if not income_account:
				# Create new category-specific income account
				income_account = m.Account(name=f"Income:{category.name}", type="income")
				session.add(income_account)
				session.flush()  # Flush to get the ID
		else:
			# Use general income account for uncategorized transactions
			income_account = session.query(m.Account).filter_by(name="Income").first()
		
		# Create balanced postings for income
		# Posting 1: Debit source account (money into bank)
		posting1 = m.Posting(
			transaction_id=transaction.id,
			account_id=transaction.source_account_id,
			debit=abs(transaction.amount),  # Debit the bank account
			credit=0
		)
		# Posting 2: Credit income account (increase income)
		posting2 = m.Posting(
			transaction_id=transaction.id,
			account_id=income_account.id,
			debit=0,
			credit=abs(transaction.amount)  # Credit the income account
		)
	
	# Add both postings to the session
	session.add(posting1)
	session.add(posting2)
	
	# Always return 2 (one debit, one credit)
	return 2


def generate_all_postings(session, limit: int = 10000) -> int:
	"""
	Generate postings for all transactions that don't have them.
	
	Processes all transactions that haven't been posted yet, creating balanced
	double-entry postings for each one. Uses batch processing for performance.
	
	Args:
		session: Database session for operations
		limit (int): Maximum number of transactions to process
		
	Returns:
		int: Number of transactions processed
		
	Note:
		Only processes transactions that don't already have postings.
		This function is idempotent - running it multiple times won't create duplicates.
	"""
	count = 0
	
	# Find transactions without postings using LEFT JOIN
	transactions = (
		session.query(m.Transaction)
		.outerjoin(m.Posting, m.Transaction.id == m.Posting.transaction_id)
		.filter(m.Posting.id.is_(None))  # No postings exist
		.limit(limit)
		.all()
	)
	
	# Generate postings for each transaction
	for txn in transactions:
		generate_postings_for_transaction(session, txn)
		count += 1
	
	return count

