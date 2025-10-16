from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget
from PySide6.QtGui import QFont

from finance_app.views.dashboard import DashboardView
from finance_app.views.import_wizard import ImportWizard
from finance_app.views.transactions import TransactionsView
from finance_app.views.rules import RulesView
from finance_app.views.reports import ReportsView


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("💰 Personal Finance Manager")
		self.resize(1200, 800)
		self.setStyleSheet(self.get_modern_style())

		# Create modern tab widget
		tabs = QTabWidget()
		tabs.setStyleSheet(self.get_tab_style())
		
		# Add tabs with icons
		tabs.addTab(DashboardView(), "🏠 Dashboard")
		tabs.addTab(ImportWizard(), "📥 Import")
		tabs.addTab(TransactionsView(), "💳 Transactions")
		tabs.addTab(RulesView(), "🎯 Rules")
		tabs.addTab(ReportsView(), "📊 Reports")

		self.setCentralWidget(tabs)
	
	def get_modern_style(self) -> str:
		"""Return modern styling for the main window."""
		return """
		QMainWindow {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 #f8f9fa, stop:1 #e9ecef);
		}
		"""
	
	def get_tab_style(self) -> str:
		"""Return modern styling for tabs."""
		return """
		QTabWidget::pane {
			border: 1px solid #dee2e6;
			border-radius: 8px;
			background: white;
			margin-top: -1px;
		}
		
		QTabWidget::tab-bar {
			alignment: left;
		}
		
		QTabBar::tab {
			background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 #f8f9fa, stop:1 #e9ecef);
			border: 1px solid #dee2e6;
			border-bottom: none;
			border-radius: 8px 8px 0 0;
			padding: 12px 20px;
			margin-right: 2px;
			font-weight: bold;
			font-size: 14px;
			min-width: 120px;
		}
		
		QTabBar::tab:selected {
			background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 #667eea, stop:1 #764ba2);
			color: white;
			border-color: #667eea;
		}
		
		QTabBar::tab:hover:!selected {
			background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
				stop:0 #e3f2fd, stop:1 #bbdefb);
			border-color: #2196f3;
		}
		
		QTabBar::tab:first {
			margin-left: 0;
		}
		"""


