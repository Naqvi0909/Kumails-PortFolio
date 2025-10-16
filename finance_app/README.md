# Personal Finance Reconciliation App

A local-first desktop application for managing personal finances with double-entry bookkeeping, transaction categorization, and visual reporting.

## Features

### ✅ Implemented (Days 1-5)

- **🎨 Modern Dashboard**: Colorful gradient UI with live stat cards and separate chart windows
- **📥 Import Wizard**: Import CSV bank statements with column mapping and preview
- **💳 Transaction Management**: View and categorize transactions with inline editing
- **🎯 Rules Engine**: Create categorization rules with regex patterns and amount ranges
- **📊 Double-Entry Postings**: Automatic generation of balanced ledger entries
- **📈 Reports**: Cashflow, category breakdown, account balances, and reconciliation reports
- **📊 Interactive Charts**: Separate chart windows with modern PyQtGraph visualizations
- **🎨 Modern UI**: Gradient backgrounds, hover effects, and responsive design

## Tech Stack

- **UI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Charts**: PyQtGraph for interactive visualizations
- **Data Processing**: pandas for CSV import
- **Packaging**: PyInstaller for Windows .exe distribution

## Installation

### Requirements
- Python 3.10+
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd P#1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the App

```bash
python finance_app/main.py
```

Or use the entry point:
```bash
python run.py
```

### Demo the Modern UI

```bash
python demo_modern_ui.py
```

This launches the app with a showcase of the modern UI features.

### First Steps

1. **Import Transactions**:
   - Go to the Import tab
   - Click "Browse CSV…" and select a bank statement (sample data in `sample_data/`)
   - Map columns: date, description, amount
   - Enter source account name (e.g., "Checking")
   - Preview and click "Import"

2. **Create Categorization Rules**:
   - Go to the Rules tab
   - Click "Add Rule"
   - Enter regex pattern (e.g., `grocery|walmart|target` for groceries)
   - Set category ID
   - Optionally set amount min/max
   - Click "Apply Rules" to categorize transactions

3. **View Transactions**:
   - Go to the Transactions tab
   - Edit categories inline using dropdowns
   - Click "Save Changes"

4. **Generate Postings**:
   - Go to the Reports tab
   - Click "Generate All Postings" to create double-entry bookkeeping entries

5. **View Dashboard**:
   - Go to Dashboard tab
   - Select time range (Last Month, Quarter, Year, All Time)
   - View cashflow and category breakdown charts

## Sample Data

Two sample CSV files are included in `sample_data/`:
- `bank_statement_1.csv` (October 2024)
- `bank_statement_2.csv` (September 2024)

Both contain realistic transaction data including:
- Salary deposits
- Rent payments
- Grocery purchases
- Utility bills
- Dining and shopping expenses

## Database Schema

### Core Tables

- **accounts**: Asset, liability, income, expense accounts
- **transactions**: Imported financial transactions
- **categories**: Hierarchical expense/income categories
- **postings**: Double-entry ledger entries (debit/credit)
- **rules**: Regex-based categorization rules
- **period_closures**: Month-end reconciliation locks

### Key Constraints

- Postings must balance: `SUM(debit - credit) = 0` per transaction
- Only one period closure per date range
- Rules evaluated by priority (ascending); first match wins

## Packaging for Distribution

### Build Windows .exe

```bash
pip install pyinstaller
pyinstaller finance_app.spec
```

The packaged app will be in `dist/FinanceApp/`.

### Run the .exe

```bash
cd dist/FinanceApp
FinanceApp.exe
```

## Project Structure

```
finance_app/
├── __init__.py
├── main.py              # Application entry point
├── db/
│   ├── context.py       # Session factory and scope manager
│   ├── init_db.py       # Database initialization and seeding
│   └── session.py       # SQLAlchemy engine creation
├── models/
│   ├── base.py          # SQLAlchemy base classes
│   └── models.py        # ORM models (Account, Transaction, etc.)
├── services/
│   ├── importer.py      # CSV import logic
│   ├── posting_generator.py  # Double-entry posting generation
│   ├── reports.py       # Report data aggregation
│   └── rules_engine.py  # Categorization rules
└── views/
    ├── dashboard.py     # Dashboard with charts
    ├── import_wizard.py # CSV import UI
    ├── main_window.py   # Main app window
    ├── reports.py       # Reports UI
    ├── rules.py         # Rules manager UI
    └── transactions.py  # Transaction list UI
```

## Development Roadmap

### Completed ✅
- [x] Day 1: Project scaffold, DB models, basic UI
- [x] Day 2: Import wizard, transaction listing
- [x] Day 3: Rules engine, inline categorization
- [x] Day 4: Double-entry postings, reconciliation
- [x] Day 5: Dashboard charts, reports, packaging

### Future Enhancements 🚀
- [ ] Period close with edit locks
- [ ] Transfer detection between accounts
- [ ] Budget tracking and forecasting
- [ ] Multi-currency support
- [ ] Attachments (receipts, statements)
- [ ] Data export (CSV, PDF reports)
- [ ] Backup and restore
- [ ] Settings UI (DB location, preferences)
- [ ] Dark mode theme

## License

MIT License - feel free to use this for your portfolio or personal projects!

## Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## Troubleshooting

### Import errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Module not found: 'finance_app'
The app adds the parent directory to sys.path automatically. Run from project root.

### Charts not displaying
Ensure pyqtgraph is installed:
```bash
pip install pyqtgraph
```

### Database locked
Close any other instances of the app. SQLite supports single-writer only.

## Credits

Built as a portfolio project showcasing:
- Desktop app development with PySide6
- Database design with SQLAlchemy
- Financial data modeling (double-entry bookkeeping)
- Data visualization with PyQtGraph
- CSV data import and transformation
- Regex pattern matching for categorization

