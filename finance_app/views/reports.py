from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
	QTableWidget, QTableWidgetItem, QDateEdit, QTextEdit
)

from finance_app.db.context import session_scope
from finance_app.models import models as m
from finance_app.services.posting_generator import generate_all_postings
from finance_app.services.reports import (
	get_cashflow_by_month,
	get_category_breakdown,
	get_account_balances,
	get_reconciliation_report
)


class ReportsView(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		# Generate postings button
		gen_btn = QPushButton("Generate All Postings")
		gen_btn.clicked.connect(self.generate_postings)
		layout.addWidget(gen_btn)

		# Date range for reports
		date_row = QHBoxLayout()
		self.start_date = QDateEdit()
		self.start_date.setDate(date.today().replace(day=1) - timedelta(days=90))
		self.end_date = QDateEdit()
		self.end_date.setDate(date.today())
		date_row.addWidget(QLabel("Start:"))
		date_row.addWidget(self.start_date)
		date_row.addWidget(QLabel("End:"))
		date_row.addWidget(self.end_date)
		layout.addLayout(date_row)

		# Report buttons
		btn_row = QHBoxLayout()
		self.cashflow_btn = QPushButton("Cashflow by Month")
		self.cashflow_btn.clicked.connect(self.show_cashflow)
		btn_row.addWidget(self.cashflow_btn)
		
		self.category_btn = QPushButton("Category Breakdown")
		self.category_btn.clicked.connect(self.show_category)
		btn_row.addWidget(self.category_btn)
		
		self.balances_btn = QPushButton("Account Balances")
		self.balances_btn.clicked.connect(self.show_balances)
		btn_row.addWidget(self.balances_btn)
		
		self.reconcile_btn = QPushButton("Reconciliation Report")
		self.reconcile_btn.clicked.connect(self.show_reconciliation)
		btn_row.addWidget(self.reconcile_btn)
		
		layout.addLayout(btn_row)

		# Output area
		self.output = QTextEdit()
		self.output.setReadOnly(True)
		layout.addWidget(self.output)

		self.setLayout(layout)

	def generate_postings(self):
		with session_scope() as s:
			count = generate_all_postings(s)
		self.output.setText(f"Generated postings for {count} transactions")

	def show_cashflow(self):
		start = self.start_date.date().toPython()
		end = self.end_date.date().toPython()
		with session_scope() as s:
			data = get_cashflow_by_month(s, start, end)
		
		text = "Cashflow by Month:\n\n"
		text += f"{'Month':<10} {'Income':>12} {'Expenses':>12} {'Net':>12}\n"
		text += "-" * 50 + "\n"
		for row in data:
			text += f"{row['month']:<10} ${row['income']:>11,.2f} ${row['expenses']:>11,.2f} ${row['net']:>11,.2f}\n"
		self.output.setText(text)

	def show_category(self):
		start = self.start_date.date().toPython()
		end = self.end_date.date().toPython()
		with session_scope() as s:
			data = get_category_breakdown(s, start, end)
		
		text = "Expenses by Category:\n\n"
		text += f"{'Category':<30} {'Amount':>12}\n"
		text += "-" * 45 + "\n"
		for row in data:
			text += f"{row['category']:<30} ${row['amount']:>11,.2f}\n"
		total = sum(r['amount'] for r in data)
		text += "-" * 45 + "\n"
		text += f"{'TOTAL':<30} ${total:>11,.2f}\n"
		self.output.setText(text)

	def show_balances(self):
		with session_scope() as s:
			data = get_account_balances(s)
		
		text = "Account Balances:\n\n"
		text += f"{'Account':<30} {'Balance':>12}\n"
		text += "-" * 45 + "\n"
		for row in data:
			text += f"{row['account']:<30} ${row['balance']:>11,.2f}\n"
		self.output.setText(text)

	def show_reconciliation(self):
		start = self.start_date.date().toPython()
		end = self.end_date.date().toPython()
		with session_scope() as s:
			data = get_reconciliation_report(s, start, end)
		
		text = f"Reconciliation Report\n"
		text += f"Period: {data['period_start']} to {data['period_end']}\n\n"
		text += f"Opening Balance:    ${data['opening_balance']:>11,.2f}\n"
		text += f"Inflows:            ${data['inflows']:>11,.2f}\n"
		text += f"Outflows:          -${data['outflows']:>11,.2f}\n"
		text += "-" * 40 + "\n"
		text += f"Closing Balance:    ${data['closing_balance']:>11,.2f}\n\n"
		text += f"Transaction Count:  {data['transaction_count']}\n"
		self.output.setText(text)

