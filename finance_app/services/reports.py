from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict

from sqlalchemy import func

from finance_app.models import models as m


def get_cashflow_by_month(session, start_date: date, end_date: date) -> List[Dict]:
	"""
	Get cashflow aggregated by month.
	Returns list of {month, income, expenses, net}
	"""
	results = (
		session.query(
			func.strftime('%Y-%m', m.Transaction.date).label('month'),
			func.sum(
				func.case(
					(m.Transaction.amount > 0, m.Transaction.amount),
					else_=0
				)
			).label('income'),
			func.sum(
				func.case(
					(m.Transaction.amount < 0, func.abs(m.Transaction.amount)),
					else_=0
				)
			).label('expenses')
		)
		.filter(m.Transaction.date.between(start_date, end_date))
		.group_by('month')
		.order_by('month')
		.all()
	)
	
	return [
		{
			'month': r.month,
			'income': float(r.income or 0),
			'expenses': float(r.expenses or 0),
			'net': float(r.income or 0) - float(r.expenses or 0)
		}
		for r in results
	]


def get_category_breakdown(session, start_date: date, end_date: date) -> List[Dict]:
	"""
	Get expenses by category for a date range.
	Returns list of {category, amount}
	"""
	results = (
		session.query(
			m.Category.name.label('category'),
			func.sum(func.abs(m.Transaction.amount)).label('amount')
		)
		.join(m.Category, m.Transaction.category_id == m.Category.id)
		.filter(m.Transaction.date.between(start_date, end_date))
		.filter(m.Transaction.amount < 0)  # Only expenses
		.group_by(m.Category.name)
		.order_by(func.sum(func.abs(m.Transaction.amount)).desc())
		.all()
	)
	
	return [
		{'category': r.category, 'amount': float(r.amount or 0)}
		for r in results
	]


def get_uncategorized_count(session) -> int:
	"""Get count of transactions without a category."""
	return session.query(m.Transaction).filter(m.Transaction.category_id.is_(None)).count()


def get_account_balances(session) -> List[Dict]:
	"""
	Get current balance for each account based on postings.
	Returns list of {account, balance}
	"""
	results = (
		session.query(
			m.Account.name.label('account'),
			(func.sum(m.Posting.debit) - func.sum(m.Posting.credit)).label('balance')
		)
		.join(m.Posting, m.Account.id == m.Posting.account_id)
		.group_by(m.Account.name)
		.all()
	)
	
	return [
		{'account': r.account, 'balance': float(r.balance or 0)}
		for r in results
	]


def get_reconciliation_report(session, period_start: date, period_end: date) -> Dict:
	"""
	Generate reconciliation report for a period.
	Returns {opening_balance, inflows, outflows, closing_balance, transaction_count}
	"""
	# Get transactions in period
	transactions = (
		session.query(m.Transaction)
		.filter(m.Transaction.date.between(period_start, period_end))
		.all()
	)
	
	inflows = sum(float(t.amount) for t in transactions if t.amount > 0)
	outflows = sum(abs(float(t.amount)) for t in transactions if t.amount < 0)
	
	# For simplicity, assume opening balance is 0 for now
	# In a real app, you'd calculate from prior period
	opening_balance = 0.0
	closing_balance = opening_balance + inflows - outflows
	
	return {
		'period_start': period_start.isoformat(),
		'period_end': period_end.isoformat(),
		'opening_balance': opening_balance,
		'inflows': inflows,
		'outflows': outflows,
		'closing_balance': closing_balance,
		'transaction_count': len(transactions)
	}

