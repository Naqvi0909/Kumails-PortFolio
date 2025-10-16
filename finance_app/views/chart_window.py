from __future__ import annotations

from datetime import date, timedelta
from typing import List, Dict

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QIcon

try:
	import pyqtgraph as pg
	CHARTS_AVAILABLE = True
except ImportError:
	CHARTS_AVAILABLE = False
	pg = None

from finance_app.db.context import session_scope
from finance_app.services.reports import get_cashflow_by_month, get_category_breakdown


class ModernChartWindow(QMainWindow):
	"""Modern chart window with gradient background and smooth animations."""
	
	def __init__(self, chart_type: str = "cashflow"):
		super().__init__()
		self.chart_type = chart_type
		self.setWindowTitle(f"📊 {chart_type.title()} Analytics")
		self.setMinimumSize(800, 600)
		self.setStyleSheet(self.get_modern_style())
		
		# Central widget
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		layout = QVBoxLayout(central_widget)
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(15)
		
		# Header
		header = self.create_header()
		layout.addWidget(header)
		
		# Chart area
		if CHARTS_AVAILABLE:
			self.chart_widget = self.create_chart_widget()
			layout.addWidget(self.chart_widget)
		else:
			no_charts_label = QLabel("📈 Charts unavailable: pyqtgraph not installed\nInstall with: pip install pyqtgraph")
			no_charts_label.setAlignment(Qt.AlignCenter)
			no_charts_label.setStyleSheet("""
				QLabel {
					color: #666;
					font-size: 16px;
					padding: 40px;
					background: #f8f9fa;
					border-radius: 10px;
					border: 2px dashed #ddd;
				}
			""")
			layout.addWidget(no_charts_label)
		
		# Load initial data
		QTimer.singleShot(100, self.load_data)
	
	def get_modern_style(self) -> str:
		"""Return modern CSS styling."""
		return """
		QMainWindow {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
				stop:0 #667eea, stop:1 #764ba2);
		}
		QWidget {
			background: transparent;
		}
		"""
	
	def create_header(self) -> QWidget:
		"""Create modern header with controls."""
		header = QWidget()
		header.setStyleSheet("""
			QWidget {
				background: rgba(255, 255, 255, 0.95);
				border-radius: 15px;
				padding: 15px;
			}
		""")
		layout = QHBoxLayout(header)
		
		# Title
		title = QLabel(f"📊 {self.chart_type.title()} Analytics")
		title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
		title.setStyleSheet("color: #2c3e50;")
		layout.addWidget(title)
		
		layout.addStretch()
		
		# Time range selector
		time_label = QLabel("Time Range:")
		time_label.setStyleSheet("color: #34495e; font-weight: bold;")
		layout.addWidget(time_label)
		
		self.time_combo = QComboBox()
		self.time_combo.addItems(["Last Month", "Last Quarter", "Last Year", "All Time"])
		self.time_combo.setStyleSheet("""
			QComboBox {
				background: white;
				border: 2px solid #e0e0e0;
				border-radius: 8px;
				padding: 8px 12px;
				font-size: 14px;
				min-width: 120px;
			}
			QComboBox:hover {
				border-color: #3498db;
			}
			QComboBox::drop-down {
				border: none;
			}
			QComboBox::down-arrow {
				image: none;
				border-left: 5px solid transparent;
				border-right: 5px solid transparent;
				border-top: 5px solid #7f8c8d;
			}
		""")
		self.time_combo.currentIndexChanged.connect(self.load_data)
		layout.addWidget(self.time_combo)
		
		# Refresh button
		refresh_btn = QPushButton("🔄 Refresh")
		refresh_btn.setStyleSheet("""
			QPushButton {
				background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
					stop:0 #3498db, stop:1 #2980b9);
				color: white;
				border: none;
				border-radius: 8px;
				padding: 10px 20px;
				font-weight: bold;
				font-size: 14px;
			}
			QPushButton:hover {
				background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
					stop:0 #5dade2, stop:1 #3498db);
			}
			QPushButton:pressed {
				background: #2980b9;
			}
		""")
		refresh_btn.clicked.connect(self.load_data)
		layout.addWidget(refresh_btn)
		
		return header
	
	def create_chart_widget(self) -> QWidget:
		"""Create the main chart widget."""
		chart_widget = QWidget()
		chart_widget.setStyleSheet("""
			QWidget {
				background: rgba(255, 255, 255, 0.95);
				border-radius: 15px;
			}
		""")
		layout = QVBoxLayout(chart_widget)
		layout.setContentsMargins(20, 20, 20, 20)
		
		if self.chart_type == "cashflow":
			self.plot_widget = self.create_cashflow_chart()
		elif self.chart_type == "categories":
			self.plot_widget = self.create_category_chart()
		else:
			self.plot_widget = pg.PlotWidget()
		
		layout.addWidget(self.plot_widget)
		return chart_widget
	
	def create_cashflow_chart(self) -> pg.PlotWidget:
		"""Create cashflow chart with modern styling."""
		plot = pg.PlotWidget(title="💰 Cashflow by Month")
		plot.setBackground('w')
		plot.setLabel('left', 'Amount ($)', color='#2c3e50', size='12pt')
		plot.setLabel('bottom', 'Month', color='#2c3e50', size='12pt')
		plot.showGrid(x=True, y=True, alpha=0.3)
		plot.setTitle("💰 Cashflow by Month", color='#2c3e50', size='16pt')
		
		# Modern color palette
		plot.getAxis('left').setPen(pg.mkPen(color='#34495e', width=2))
		plot.getAxis('bottom').setPen(pg.mkPen(color='#34495e', width=2))
		
		return plot
	
	def create_category_chart(self) -> pg.PlotWidget:
		"""Create category breakdown chart."""
		plot = pg.PlotWidget(title="📊 Top Expense Categories")
		plot.setBackground('w')
		plot.setLabel('left', 'Category', color='#2c3e50', size='12pt')
		plot.setLabel('bottom', 'Amount ($)', color='#2c3e50', size='12pt')
		plot.setTitle("📊 Top Expense Categories", color='#2c3e50', size='16pt')
		
		plot.getAxis('left').setPen(pg.mkPen(color='#34495e', width=2))
		plot.getAxis('bottom').setPen(pg.mkPen(color='#34495e', width=2))
		
		return plot
	
	def get_date_range(self) -> tuple[date, date]:
		"""Get date range based on selection."""
		today = date.today()
		range_type = self.time_combo.currentText()
		
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
	
	def load_data(self):
		"""Load and display chart data."""
		if not CHARTS_AVAILABLE:
			return
		
		start, end = self.get_date_range()
		
		with session_scope() as s:
			if self.chart_type == "cashflow":
				self.load_cashflow_data(s, start, end)
			elif self.chart_type == "categories":
				self.load_category_data(s, start, end)
	
	def load_cashflow_data(self, session, start: date, end: date):
		"""Load cashflow data into chart."""
		from finance_app.services.reports import get_cashflow_by_month
		
		data = get_cashflow_by_month(session, start, end)
		if not data:
			return
		
		self.plot_widget.clear()
		
		months = list(range(len(data)))
		income = [d['income'] for d in data]
		expenses = [d['expenses'] for d in data]
		net = [d['net'] for d in data]
		
		# Modern colors
		colors = {
			'income': '#27ae60',    # Green
			'expenses': '#e74c3c',   # Red
			'net': '#3498db'        # Blue
		}
		
		# Create bars with modern styling
		income_bars = pg.BarGraphItem(
			x=[m - 0.25 for m in months], 
			height=income, 
			width=0.2, 
			brush=colors['income'], 
			name='💰 Income'
		)
		expense_bars = pg.BarGraphItem(
			x=months, 
			height=expenses, 
			width=0.2, 
			brush=colors['expenses'], 
			name='💸 Expenses'
		)
		net_bars = pg.BarGraphItem(
			x=[m + 0.25 for m in months], 
			height=net, 
			width=0.2, 
			brush=colors['net'], 
			name='📈 Net'
		)
		
		self.plot_widget.addItem(income_bars)
		self.plot_widget.addItem(expense_bars)
		self.plot_widget.addItem(net_bars)
		
		# Add legend
		legend = self.plot_widget.addLegend()
		legend.setBrush(pg.mkBrush(color=(255, 255, 255, 200)))
		legend.setPen(pg.mkPen(color=(200, 200, 200)))
	
	def load_category_data(self, session, start: date, end: date):
		"""Load category data into chart."""
		from finance_app.services.reports import get_category_breakdown
		
		data = get_category_breakdown(session, start, end)
		if not data:
			return
		
		self.plot_widget.clear()
		
		top_5 = data[:5]
		if not top_5:
			return
		
		y_pos = list(range(len(top_5)))
		amounts = [d['amount'] for d in top_5]
		categories = [d['category'] for d in top_5]
		
		# Modern gradient colors
		colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db']
		
		bars = pg.BarGraphItem(
			x=amounts, 
			y=y_pos, 
			height=0.8, 
			brush=colors[:len(top_5)], 
			orientation='horizontal'
		)
		self.plot_widget.addItem(bars)
		
		# Add category labels
		axis = self.plot_widget.getAxis('left')
		axis.setTicks([[(i, f"📊 {categories[i]}") for i in range(len(top_5))]])


class CashflowChartWindow(ModernChartWindow):
	"""Dedicated cashflow chart window."""
	def __init__(self):
		super().__init__("cashflow")


class CategoryChartWindow(ModernChartWindow):
	"""Dedicated category chart window."""
	def __init__(self):
		super().__init__("categories")
