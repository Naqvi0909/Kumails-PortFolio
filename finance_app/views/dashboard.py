from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, 
	QGridLayout, QFrame, QScrollArea, QSizePolicy
)
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect

try:
	import pyqtgraph as pg
	CHARTS_AVAILABLE = True
except ImportError:
	CHARTS_AVAILABLE = False
	pg = None

from finance_app.db.context import session_scope
from finance_app.services.reports import (
	get_cashflow_by_month,
	get_category_breakdown,
	get_uncategorized_count,
	get_account_balances
)


class DashboardView(QWidget):
	def __init__(self) -> None:
		super().__init__()
		self.setStyleSheet(self.get_modern_style())
		
		# Main layout
		layout = QVBoxLayout()
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(20)
		
		# Header section
		header = self.create_header()
		layout.addWidget(header)
		
		# Stats cards
		stats_section = self.create_stats_section()
		layout.addWidget(stats_section)
		
		# Quick actions
		actions_section = self.create_actions_section()
		layout.addWidget(actions_section)
		
		# Chart buttons
		charts_section = self.create_charts_section()
		layout.addWidget(charts_section)
		
		layout.addStretch()
		self.setLayout(layout)
		
		# Load initial data
		QTimer.singleShot(100, self.refresh)
	
	def get_modern_style(self) -> str:
		"""Return modern CSS styling for the dashboard."""
		return """
		QWidget {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 #f8f9fa, stop:1 #e9ecef);
			font-family: 'Segoe UI', Arial, sans-serif;
		}
		"""
	
	def create_header(self) -> QWidget:
		"""Create modern header with title and controls."""
		header = QFrame()
		header.setStyleSheet("""
			QFrame {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
					stop:0 #667eea, stop:1 #764ba2);
				border-radius: 15px;
				padding: 20px;
			}
		""")
		layout = QHBoxLayout(header)
		layout.setContentsMargins(20, 20, 20, 20)
		
		# Title
		title = QLabel("🏠 Financial Dashboard")
		title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
		title.setStyleSheet("color: white;")
		layout.addWidget(title)
		
		layout.addStretch()
		
		# Time range selector
		time_label = QLabel("📅 Time Range:")
		time_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
		time_label.setStyleSheet("color: white;")
		layout.addWidget(time_label)
		
		self.range_combo = QComboBox()
		self.range_combo.addItems(["Last Month", "Last Quarter", "Last Year", "All Time"])
		self.range_combo.setStyleSheet("""
			QComboBox {
				background: rgba(255, 255, 255, 0.9);
				border: 2px solid rgba(255, 255, 255, 0.3);
				border-radius: 8px;
				padding: 8px 12px;
				font-size: 14px;
				font-weight: bold;
				min-width: 140px;
			}
			QComboBox:hover {
				background: white;
				border-color: rgba(255, 255, 255, 0.6);
			}
			QComboBox::drop-down {
				border: none;
				width: 20px;
			}
			QComboBox::down-arrow {
				image: none;
				border-left: 5px solid transparent;
				border-right: 5px solid transparent;
				border-top: 5px solid #667eea;
			}
		""")
		self.range_combo.currentIndexChanged.connect(self.refresh)
		layout.addWidget(self.range_combo)
		
		# Refresh button
		self.refresh_btn = QPushButton("🔄 Refresh")
		self.refresh_btn.setStyleSheet("""
			QPushButton {
				background: rgba(255, 255, 255, 0.2);
				color: white;
				border: 2px solid rgba(255, 255, 255, 0.3);
				border-radius: 8px;
				padding: 10px 20px;
				font-weight: bold;
				font-size: 14px;
			}
			QPushButton:hover {
				background: rgba(255, 255, 255, 0.3);
				border-color: rgba(255, 255, 255, 0.6);
			}
			QPushButton:pressed {
				background: rgba(255, 255, 255, 0.1);
			}
		""")
		self.refresh_btn.clicked.connect(self.refresh)
		layout.addWidget(self.refresh_btn)
		
		return header
	
	def create_stats_section(self) -> QWidget:
		"""Create stats cards section."""
		section = QFrame()
		section.setStyleSheet("""
			QFrame {
				background: white;
				border-radius: 15px;
				padding: 20px;
			}
		""")
		layout = QHBoxLayout(section)
		layout.setSpacing(20)
		
		# Stats cards
		self.balance_card = self.create_stat_card(
			"💰 Total Balance", "$0.00", "#27ae60", "💳"
		)
		layout.addWidget(self.balance_card)
		
		self.uncat_card = self.create_stat_card(
			"📝 Uncategorized", "0", "#e74c3c", "⚠️"
		)
		layout.addWidget(self.uncat_card)
		
		self.transactions_card = self.create_stat_card(
			"📊 Transactions", "0", "#3498db", "📈"
		)
		layout.addWidget(self.transactions_card)
		
		return section
	
	def create_stat_card(self, title: str, value: str, color: str, icon: str) -> QFrame:
		"""Create a modern stat card."""
		card = QFrame()
		card.setStyleSheet(f"""
			QFrame {{
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
					stop:0 {color}, stop:1 {color}dd);
				border-radius: 12px;
				padding: 20px;
			}}
		""")
		layout = QVBoxLayout(card)
		layout.setSpacing(10)
		
		# Icon and title
		title_label = QLabel(f"{icon} {title}")
		title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
		title_label.setStyleSheet("color: white;")
		title_label.setAlignment(Qt.AlignCenter)
		layout.addWidget(title_label)
		
		# Value
		value_label = QLabel(value)
		value_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
		value_label.setStyleSheet("color: white;")
		value_label.setAlignment(Qt.AlignCenter)
		value_label.setObjectName("value")
		layout.addWidget(value_label)
		
		return card
	
	def create_actions_section(self) -> QWidget:
		"""Create quick actions section."""
		section = QFrame()
		section.setStyleSheet("""
			QFrame {
				background: white;
				border-radius: 15px;
				padding: 20px;
			}
		""")
		layout = QVBoxLayout(section)
		
		# Section title
		title = QLabel("⚡ Quick Actions")
		title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
		title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
		layout.addWidget(title)
		
		# Action buttons
		buttons_layout = QHBoxLayout()
		
		# Import button
		import_btn = QPushButton("📥 Import CSV")
		import_btn.setStyleSheet(self.get_action_button_style("#3498db"))
		import_btn.clicked.connect(self.open_import)
		buttons_layout.addWidget(import_btn)
		
		# Rules button
		rules_btn = QPushButton("🎯 Manage Rules")
		rules_btn.setStyleSheet(self.get_action_button_style("#e67e22"))
		rules_btn.clicked.connect(self.open_rules)
		buttons_layout.addWidget(rules_btn)
		
		# Reports button
		reports_btn = QPushButton("📊 View Reports")
		reports_btn.setStyleSheet(self.get_action_button_style("#9b59b6"))
		reports_btn.clicked.connect(self.open_reports)
		buttons_layout.addWidget(reports_btn)
		
		layout.addLayout(buttons_layout)
		return section
	
	def get_action_button_style(self, color: str) -> str:
		"""Get style for action buttons."""
		return f"""
		QPushButton {{
			background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 {color}, stop:1 {color}dd);
			color: white;
			border: none;
			border-radius: 10px;
			padding: 15px 25px;
			font-weight: bold;
			font-size: 14px;
			min-width: 120px;
		}}
		QPushButton:hover {{
			background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 {color}ee, stop:1 {color});
		}}
		QPushButton:pressed {{
			background: {color};
		}}
		"""
	
	def create_charts_section(self) -> QWidget:
		"""Create charts section with modern buttons."""
		section = QFrame()
		section.setStyleSheet("""
			QFrame {
				background: white;
				border-radius: 15px;
				padding: 20px;
			}
		""")
		layout = QVBoxLayout(section)
		
		# Section title
		title = QLabel("📈 Analytics & Charts")
		title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
		title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
		layout.addWidget(title)
		
		# Chart buttons
		charts_layout = QHBoxLayout()
		
		# Cashflow chart button
		cashflow_btn = QPushButton("💰 Cashflow Analysis")
		cashflow_btn.setStyleSheet(self.get_chart_button_style("#27ae60"))
		cashflow_btn.clicked.connect(self.open_cashflow_chart)
		charts_layout.addWidget(cashflow_btn)
		
		# Category chart button
		category_btn = QPushButton("📊 Category Breakdown")
		category_btn.setStyleSheet(self.get_chart_button_style("#e74c3c"))
		category_btn.clicked.connect(self.open_category_chart)
		charts_layout.addWidget(category_btn)
		
		layout.addLayout(charts_layout)
		return section
	
	def get_chart_button_style(self, color: str) -> str:
		"""Get style for chart buttons."""
		return f"""
		QPushButton {{
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 {color}, stop:1 {color}cc);
			color: white;
			border: none;
			border-radius: 12px;
			padding: 20px 30px;
			font-weight: bold;
			font-size: 16px;
			min-width: 200px;
			min-height: 60px;
		}}
		QPushButton:hover {{
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 {color}ee, stop:1 {color}dd);
			transform: scale(1.05);
		}}
		QPushButton:pressed {{
			background: {color};
		}}
		"""
	
	def open_import(self):
		"""Open import tab (placeholder)."""
		# This would switch to the import tab in the main window
		pass
	
	def open_rules(self):
		"""Open rules tab (placeholder)."""
		# This would switch to the rules tab in the main window
		pass
	
	def open_reports(self):
		"""Open reports tab (placeholder)."""
		# This would switch to the reports tab in the main window
		pass
	
	def open_cashflow_chart(self):
		"""Open cashflow chart in separate window."""
		from finance_app.views.chart_window import CashflowChartWindow
		self.cashflow_window = CashflowChartWindow()
		self.cashflow_window.show()
	
	def open_category_chart(self):
		"""Open category chart in separate window."""
		from finance_app.views.chart_window import CategoryChartWindow
		self.category_window = CategoryChartWindow()
		self.category_window.show()

	def get_date_range(self):
		"""Get date range based on selection."""
		today = date.today()
		range_type = self.range_combo.currentText()
		
		if range_type == "Last Month":
			start = today.replace(day=1)
			end = today
		elif range_type == "Last Quarter":
			start = today - timedelta(days=90)
			end = today
		elif range_type == "Last Year":
			start = today - timedelta(days=365)
			end = today
		else:  # All Time
			start = date(2000, 1, 1)
			end = today
		
		return start, end

	def refresh(self):
		"""Refresh dashboard data and update stats cards."""
		start, end = self.get_date_range()
		
		with session_scope() as s:
			# Update stats cards
			uncat_count = get_uncategorized_count(s)
			self.update_stat_card(self.uncat_card, str(uncat_count))
			
			balances = get_account_balances(s)
			total_balance = sum(b['balance'] for b in balances if 'Checking' in b['account'] or 'Savings' in b['account'])
			self.update_stat_card(self.balance_card, f"${total_balance:,.2f}")
			
			# Get transaction count
			from finance_app.models import models as m
			transaction_count = s.query(m.Transaction).count()
			self.update_stat_card(self.transactions_card, str(transaction_count))
	
	def update_stat_card(self, card: QFrame, value: str):
		"""Update the value in a stat card."""
		value_label = card.findChild(QLabel, "value")
		if value_label:
			value_label.setText(value)


