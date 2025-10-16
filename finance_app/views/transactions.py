from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox

from finance_app.db.context import session_scope
from finance_app.models import models as m


class TransactionsView(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		toolbar = QHBoxLayout()
		self.refresh_btn = QPushButton("Refresh")
		self.refresh_btn.clicked.connect(self.refresh)
		toolbar.addWidget(self.refresh_btn)
		self.save_btn = QPushButton("Save Changes")
		self.save_btn.clicked.connect(self.save_changes)
		toolbar.addWidget(self.save_btn)
		layout.addLayout(toolbar)

		self.table = QTableWidget(0, 5)
		self.table.setHorizontalHeaderLabels(["Date", "Description", "Amount", "Source", "Category"])
		layout.addWidget(self.table)

		self.setLayout(layout)
		self._pending_category_updates: list[tuple[int, int]] = []  # (row, category_id)
		self.refresh()

	def refresh(self):
		self.table.setRowCount(0)
		with session_scope() as s:
			categories = {c.id: c.name for c in s.query(m.Category).order_by(m.Category.name).all()}
			rows = (
				s.query(m.Transaction, m.Account)
				.join(m.Account, m.Account.id == m.Transaction.source_account_id)
				.order_by(m.Transaction.date.desc())
				.limit(500)
				.all()
			)
			for i, (txn, acct) in enumerate(rows):
				self.table.insertRow(i)
				self.table.setItem(i, 0, QTableWidgetItem(str(txn.date)))
				self.table.setItem(i, 1, QTableWidgetItem(txn.description))
				self.table.setItem(i, 2, QTableWidgetItem(f"{float(txn.amount):.2f}"))
				self.table.setItem(i, 3, QTableWidgetItem(acct.name))
				combo = QComboBox()
				combo.addItem("", -1)
				for cid, name in categories.items():
					combo.addItem(name, cid)
				if txn.category_id:
					idx = combo.findData(txn.category_id)
					combo.setCurrentIndex(idx if idx >= 0 else 0)
				combo.currentIndexChanged.connect(lambda _i, row=i, w=combo: self._on_category_changed(row, w))
				self.table.setCellWidget(i, 4, combo)

	def _on_category_changed(self, row: int, widget: QComboBox):
		category_id = widget.currentData()
		self._pending_category_updates.append((row, category_id))

	def save_changes(self):
		if not self._pending_category_updates:
			return
		ids_to_update: list[tuple[int, int]] = []  # (txn_id, category_id)
		with session_scope() as s:
			rows = (
				s.query(m.Transaction.id)
				.order_by(m.Transaction.date.desc())
				.limit(500)
				.all()
			)
			id_by_row = [row[0] for row in rows]
			for row_idx, category_id in self._pending_category_updates:
				if 0 <= row_idx < len(id_by_row):
					ids_to_update.append((id_by_row[row_idx], category_id if isinstance(category_id, int) and category_id > 0 else None))
			for txn_id, category_id in ids_to_update:
				txn = s.get(m.Transaction, txn_id)
				if txn is not None:
					txn.category_id = category_id

		self._pending_category_updates.clear()
		self.refresh()


