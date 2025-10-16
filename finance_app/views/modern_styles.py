"""
Modern styling utilities for consistent UI across all views.
"""

def get_card_style() -> str:
	"""Get style for card containers."""
	return """
	QFrame {
		background: white;
		border-radius: 15px;
		padding: 20px;
		border: 1px solid #e0e0e0;
	}
	"""

def get_button_style(color: str, size: str = "medium") -> str:
	"""Get modern button style."""
	sizes = {
		"small": "8px 16px",
		"medium": "12px 24px", 
		"large": "16px 32px"
	}
	padding = sizes.get(size, sizes["medium"])
	
	return f"""
	QPushButton {{
		background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
			stop:0 {color}, stop:1 {color}dd);
		color: white;
		border: none;
		border-radius: 8px;
		padding: {padding};
		font-weight: bold;
		font-size: 14px;
	}}
	QPushButton:hover {{
		background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
			stop:0 {color}ee, stop:1 {color});
	}}
	QPushButton:pressed {{
		background: {color};
	}}
	"""

def get_input_style() -> str:
	"""Get style for input fields."""
	return """
	QLineEdit, QComboBox, QSpinBox {
		background: white;
		border: 2px solid #e0e0e0;
		border-radius: 8px;
		padding: 8px 12px;
		font-size: 14px;
	}
	QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
		border-color: #3498db;
	}
	QLineEdit:hover, QComboBox:hover, QSpinBox:hover {
		border-color: #bdc3c7;
	}
	"""

def get_table_style() -> str:
	"""Get style for tables."""
	return """
	QTableWidget {
		background: white;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		gridline-color: #f0f0f0;
		selection-background-color: #e3f2fd;
	}
	QTableWidget::item {
		padding: 8px;
		border: none;
	}
	QTableWidget::item:selected {
		background: #e3f2fd;
		color: #1976d2;
	}
	QHeaderView::section {
		background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
			stop:0 #f8f9fa, stop:1 #e9ecef);
		border: 1px solid #dee2e6;
		padding: 8px;
		font-weight: bold;
	}
	"""

def get_section_title_style() -> str:
	"""Get style for section titles."""
	return """
	QLabel {
		color: #2c3e50;
		font-weight: bold;
		font-size: 16px;
		margin-bottom: 10px;
	}
	"""

def get_modern_colors() -> dict:
	"""Get modern color palette."""
	return {
		"primary": "#3498db",
		"secondary": "#2ecc71", 
		"success": "#27ae60",
		"warning": "#f39c12",
		"danger": "#e74c3c",
		"info": "#17a2b8",
		"light": "#f8f9fa",
		"dark": "#343a40",
		"muted": "#6c757d"
	}
