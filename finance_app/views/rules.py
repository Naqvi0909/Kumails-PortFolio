from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QSpinBox, QCheckBox

from finance_app.db.context import session_scope
from finance_app.models import models as m
from finance_app.services.rules_engine import dry_run_matches, apply_rules


class RulesView(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		toolbar = QHBoxLayout()
		self.refresh_btn = QPushButton("Refresh")
		self.refresh_btn.clicked.connect(self.refresh)
		toolbar.addWidget(self.refresh_btn)
		self.add_btn = QPushButton("Add Rule")
		self.add_btn.clicked.connect(self.add_rule)
		toolbar.addWidget(self.add_btn)
		self.dry_run_btn = QPushButton("Dry Run")
		self.dry_run_btn.clicked.connect(self.dry_run)
		toolbar.addWidget(self.dry_run_btn)
		self.apply_btn = QPushButton("Apply Rules")
		self.apply_btn.clicked.connect(self.apply)
		toolbar.addWidget(self.apply_btn)
		layout.addLayout(toolbar)

		self.table = QTableWidget(0, 6)
		self.table.setHorizontalHeaderLabels(["Pattern", "CategoryId", "Min", "Max", "Priority", "Active"])
		layout.addWidget(self.table)

		self.result_label = QLabel("")
		layout.addWidget(self.result_label)

		self.setLayout(layout)
		self.refresh()

	def refresh(self):
		self.table.setRowCount(0)
		with session_scope() as s:
			rules = s.query(m.Rule).order_by(m.Rule.priority.asc()).all()
			for i, r in enumerate(rules):
				self.table.insertRow(i)
				pattern = QLineEdit(r.pattern)
				self.table.setCellWidget(i, 0, pattern)
				self.table.setItem(i, 1, QTableWidgetItem(str(r.category_id)))
				minv = QLineEdit("" if r.amount_min is None else f"{float(r.amount_min):.2f}")
				self.table.setCellWidget(i, 2, minv)
				maxv = QLineEdit("" if r.amount_max is None else f"{float(r.amount_max):.2f}")
				self.table.setCellWidget(i, 3, maxv)
				prio = QSpinBox()
				prio.setRange(0, 100000)
				prio.setValue(r.priority)
				self.table.setCellWidget(i, 4, prio)
				active = QCheckBox()
				active.setChecked(r.active)
				self.table.setCellWidget(i, 5, active)

	def add_rule(self):
		with session_scope() as s:
			r = m.Rule(pattern="", category_id=s.query(m.Category.id).first()[0], priority=100, active=True)
			s.add(r)
		self.refresh()

	def dry_run(self):
		with session_scope() as s:
			matches = dry_run_matches(s, limit=500)
		self.result_label.setText(f"Dry run: {len(matches)} matches")

	def apply(self):
		with session_scope() as s:
			updated = apply_rules(s)
		self.result_label.setText(f"Applied rules to {updated} transactions")
		self.refresh()


