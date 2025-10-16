"""
Rules engine for automated transaction categorization.

This module implements a regex-based rules engine that automatically categorizes
transactions based on description patterns and optional amount ranges. Rules are
evaluated in priority order, and the first matching rule is applied.

Key Features:
- Regex pattern matching on transaction descriptions
- Optional amount range filtering (min/max)
- Priority-based rule evaluation
- Dry-run capability to preview matches
- Batch processing for performance

Key Functions:
- RuleMatch: Data class for rule match results
- _rule_matches(): Check if a rule matches a transaction
- dry_run_matches(): Preview rule matches without applying
- apply_rules(): Apply rules to categorize transactions
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from finance_app.models import models as m


@dataclass
class RuleMatch:
	"""
	Result of a rule match during dry-run analysis.
	
	Represents a transaction that would be categorized by a specific rule,
	used for previewing rule effects before applying them.
	
	Attributes:
		transaction_id (int): ID of the transaction that would be matched
		rule_id (int): ID of the rule that would match
		category_id (int): ID of the category that would be assigned
	"""
	transaction_id: int
	rule_id: int
	category_id: int


def _rule_matches(rule: m.Rule, description: str, amount: float) -> bool:
	"""
	Check if a rule matches a transaction.
	
	Evaluates a rule against a transaction's description and amount to determine
	if the rule should be applied. Rules must be active and match all criteria.
	
	Args:
		rule (Rule): The rule to evaluate
		description (str): Transaction description text
		amount (float): Transaction amount
		
	Returns:
		bool: True if rule matches, False otherwise
		
	Criteria:
		- Rule must be active
		- Description must match regex pattern (case-insensitive)
		- Amount must be within min/max range (if specified)
	"""
	# Rule must be active
	if not rule.active:
		return False
	
	# Check regex pattern match (case-insensitive)
	if not re.search(rule.pattern, description, flags=re.IGNORECASE):
		return False
	
	# Check minimum amount constraint
	if rule.amount_min is not None and amount < float(rule.amount_min):
		return False
	
	# Check maximum amount constraint
	if rule.amount_max is not None and amount > float(rule.amount_max):
		return False
	
	return True


def dry_run_matches(session, limit: int = 1000) -> List[RuleMatch]:
	"""
	Preview rule matches without applying them.
	
	Analyzes uncategorized transactions against active rules to show what
	categorizations would be applied. Useful for testing rule effectiveness.
	
	Args:
		session: Database session for operations
		limit (int): Maximum number of transactions to analyze
		
	Returns:
		List[RuleMatch]: List of transactions that would be matched by rules
		
	Note:
		Only analyzes uncategorized transactions (category_id is None)
		Rules are evaluated in priority order (lower priority number = higher precedence)
	"""
	results: List[RuleMatch] = []
	
	# Get uncategorized transactions (most recent first)
	transactions = (
		session.query(m.Transaction)
		.filter(m.Transaction.category_id.is_(None))
		.order_by(m.Transaction.date.desc())
		.limit(limit)
		.all()
	)
	
	# Get active rules in priority order
	rules = session.query(m.Rule).filter(m.Rule.active.is_(True)).order_by(m.Rule.priority.asc()).all()
	
	# Evaluate each transaction against rules
	for txn in transactions:
		for rule in rules:
			if _rule_matches(rule, txn.description, float(txn.amount)):
				# First matching rule wins (due to priority ordering)
				results.append(RuleMatch(
					transaction_id=txn.id, 
					rule_id=rule.id, 
					category_id=rule.category_id
				))
				break  # Stop at first match
	
	return results


def apply_rules(session, batch_size: int = 1000) -> int:
	"""
	Apply rules to categorize uncategorized transactions.
	
	Processes uncategorized transactions in batches, applying the first matching
	rule to each transaction. Uses batch processing for memory efficiency.
	
	Args:
		session: Database session for operations
		batch_size (int): Number of transactions to process per batch
		
	Returns:
		int: Number of transactions successfully categorized
		
	Note:
		Only processes uncategorized transactions (category_id is None)
		Rules are evaluated in priority order (lower priority number = higher precedence)
		First matching rule is applied, subsequent rules are ignored
	"""
	updated = 0
	
	# Get active rules in priority order
	rules = session.query(m.Rule).filter(m.Rule.active.is_(True)).order_by(m.Rule.priority.asc()).all()
	
	# Query for uncategorized transactions
	q = session.query(m.Transaction).filter(m.Transaction.category_id.is_(None)).order_by(m.Transaction.date.asc())
	
	# Process transactions in batches for memory efficiency
	for txn in q.yield_per(batch_size):
		# Try each rule in priority order
		for rule in rules:
			if _rule_matches(rule, txn.description, float(txn.amount)):
				# Apply the first matching rule
				txn.category_id = rule.category_id
				updated += 1
				break  # Stop at first match
	
	return updated


