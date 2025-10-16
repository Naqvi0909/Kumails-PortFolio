from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QPushButton,
	QLabel,
	QFileDialog,
	QComboBox,
	QTableWidget,
	QTableWidgetItem,
)

from finance_app.db.context import session_scope
from finance_app.services.importer import preview_dataframe, import_transactions, ImportMapping


class ImportWizard(QWidget):
	def __init__(self) -> None:
		super().__init__()
		layout = QVBoxLayout()

		file_row = QHBoxLayout()
		self.file_label = QLabel("No file selected")
		self.browse_btn = QPushButton("Browse CSV…")
		self.browse_btn.clicked.connect(self.choose_file)
		file_row.addWidget(self.file_label)
		file_row.addWidget(self.browse_btn)
		layout.addLayout(file_row)

		map_row = QHBoxLayout()
		self.date_combo = QComboBox(); self.date_combo.setPlaceholderText("Date column")
		self.desc_combo = QComboBox(); self.desc_combo.setPlaceholderText("Description column")
		self.amount_combo = QComboBox(); self.amount_combo.setPlaceholderText("Amount column")
		self.source_combo = QComboBox(); self.source_combo.setEditable(True); self.source_combo.setPlaceholderText("Source account name")
		for w in (self.date_combo, self.desc_combo, self.amount_combo, self.source_combo):
			map_row.addWidget(w)
		layout.addLayout(map_row)

		self.preview_table = QTableWidget(0, 0)
		layout.addWidget(self.preview_table)

		actions = QHBoxLayout()
		self.import_btn = QPushButton("Import")
		self.import_btn.clicked.connect(self.do_import)
		actions.addWidget(self.import_btn)
		layout.addLayout(actions)

		self.setLayout(layout)
		self.csv_path: Path | None = None

	def choose_file(self):
		fname, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
		if not fname:
			return
		self.csv_path = Path(fname)
		self.file_label.setText(self.csv_path.name)
		df = preview_dataframe(str(self.csv_path))
		self.date_combo.clear(); self.desc_combo.clear(); self.amount_combo.clear()
		self.date_combo.addItems(list(df.columns))
		self.desc_combo.addItems(list(df.columns))
		self.amount_combo.addItems(list(df.columns))
		self.preview_table.setColumnCount(len(df.columns))
		self.preview_table.setHorizontalHeaderLabels(list(df.columns))
		self.preview_table.setRowCount(len(df.index))
		for i, (_, row) in enumerate(df.iterrows()):
			for j, val in enumerate(row):
				self.preview_table.setItem(i, j, QTableWidgetItem(str(val)))

	def do_import(self):
		if not self.csv_path:
			return
		mapping = ImportMapping(
			date_col=self.date_combo.currentText(),
			description_col=self.desc_combo.currentText(),
			amount_col=self.amount_combo.currentText(),
			source_account_name=self.source_combo.currentText() or "Checking",
		)
		with session_scope() as s:
			created = import_transactions(s, str(self.csv_path), mapping)
		# Feedback could be improved with dialogs; simple label update for now
		self.file_label.setText(f"Imported {created} transactions from {self.csv_path.name}")


