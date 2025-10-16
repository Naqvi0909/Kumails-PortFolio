# Feature Showcase

## 🏠 Dashboard

### Interactive Charts
- **Cashflow by Month**: Grouped bar chart showing Income (green), Expenses (red), and Net (blue)
- **Top 5 Categories**: Horizontal bar chart of biggest expense categories
- **Time Range Selector**: Last Month, Quarter, Year, or All Time
- **Live Stats**: Uncategorized transaction count and total account balance

### Technical Implementation
- PyQtGraph for high-performance interactive charts
- SQL aggregations with date grouping and category rollups
- Real-time refresh on filter change
- White background for professional appearance

---

## 📥 Import Wizard

### Flexible CSV Import
- **File Browser**: Native file dialog for CSV selection
- **Column Mapping**: Dropdown selectors for date, description, amount columns
- **Source Account**: Create or select existing account
- **Data Preview**: First 50 rows displayed in table before import
- **Batch Import**: Processes entire file with validation

### Technical Implementation
- pandas for robust CSV parsing
- Multiple date format support (YYYY-MM-DD, MM/DD/YYYY)
- Auto-create accounts if not exist
- Error handling for malformed data
- Progress feedback via label updates

---

## 💰 Transactions View

### Transaction Management
- **Paginated Table**: 500 most recent transactions sorted by date
- **Inline Category Editing**: Dropdown in each row for quick categorization
- **Batch Save**: Apply all changes with single click
- **Real-time Filtering**: Search and filter (future enhancement)

### Technical Implementation
- QTableWidget with embedded QComboBox widgets
- Session scope for safe batch updates
- Join queries for account names
- Pending changes tracked before save

---

## 🎯 Rules Manager

### Smart Categorization
- **Regex Patterns**: Full regex support for flexible matching (e.g., `grocery|walmart|target`)
- **Amount Ranges**: Optional min/max filters for amount-based rules
- **Priority Ordering**: Lower priority = higher precedence
- **Active/Inactive Toggle**: Enable/disable rules without deletion
- **Dry Run**: Preview matches before applying
- **Batch Apply**: Categorize all uncategorized transactions in one click

### Technical Implementation
- Python regex module with case-insensitive matching
- Priority-sorted rule evaluation (first match wins)
- Bulk update queries for performance
- Match count feedback

---

## 📊 Reports

### Report Types

#### 1. Cashflow by Month
- Monthly aggregation of income, expenses, and net
- Formatted as table with currency symbols
- Date range filtering

#### 2. Category Breakdown
- Top expense categories with amounts
- Total sum at bottom
- Sorted by amount descending

#### 3. Account Balances
- Current balance per account from ledger postings
- Debit - Credit calculations
- All account types (asset, liability, income, expense)

#### 4. Reconciliation Report
- Period-based summary (start/end dates)
- Opening balance, inflows, outflows, closing balance
- Transaction count for verification

### Technical Implementation
- SQL aggregations with GROUP BY and window functions
- Date range filtering with BETWEEN
- SQLAlchemy query builder for flexibility
- Formatted output with right-aligned numbers

---

## 📚 Double-Entry Postings

### Automatic Ledger Generation
- **Two Postings Per Transaction**: Source account ↔ category account
- **Balanced Entries**: Debit always equals credit
- **Category Account Creation**: Auto-creates "Expense:Groceries", "Income:Salary", etc.
- **Batch Generation**: Process all transactions at once

### Posting Rules
- **Expenses (amount < 0)**:
  - Credit source account (money out)
  - Debit expense account
- **Income (amount > 0)**:
  - Debit source account (money in)
  - Credit income account

### Technical Implementation
- Service layer with posting_generator.py
- Check constraint ensures non-negative debit/credit
- Orphan deletion when transaction removed
- Session flush for ID generation

---

## 🎨 UI/UX Highlights

### Professional Design
- **Tabbed Interface**: Clear navigation with 5 main sections
- **Consistent Layout**: Toolbar buttons, data tables, action buttons
- **Visual Feedback**: Labels update after operations
- **Keyboard-Friendly**: Tab navigation, Enter to submit

### Widget Choices
- **QTableWidget**: Familiar spreadsheet-like data view
- **QComboBox**: Easy dropdown selections
- **QPushButton**: Clear call-to-action buttons
- **QLabel**: Status and instruction text
- **PyQtGraph**: Professional interactive charts

---

## 🔧 Technical Architecture

### Database Layer
- **SQLAlchemy ORM**: Type-safe model definitions
- **Session Management**: Context manager for automatic commit/rollback
- **Constraints**: Foreign keys, unique, check constraints
- **Indexes**: On foreign keys and date columns

### Service Layer
- **Importer**: CSV parsing and validation
- **Rules Engine**: Pattern matching and categorization
- **Posting Generator**: Double-entry logic
- **Reports**: Data aggregation and formatting

### View Layer
- **PySide6 Widgets**: Custom Qt widgets per feature
- **Signal/Slot**: Event-driven architecture
- **Layout Managers**: VBox, HBox, Grid for responsive design
- **PyQtGraph**: Chart widgets for visualization

---

## 📦 Packaging & Distribution

### PyInstaller Build
- **Spec File**: Configured for PySide6, SQLAlchemy, pandas, pyqtgraph
- **Single-Folder Distribution**: All dependencies bundled
- **Windows .exe**: No Python installation required
- **Icon Support**: Ready for custom app icon (future)

### Build Command
```bash
pyinstaller finance_app.spec
```

### Distribution
```
dist/FinanceApp/
├── FinanceApp.exe
├── PySide6/ (Qt libraries)
├── pandas/ (data libraries)
└── ... (other dependencies)
```

---

## 🚀 Performance Highlights

### Query Optimization
- **Indexed Queries**: Foreign keys indexed automatically
- **Batch Operations**: Apply rules to 500+ transactions in < 1 second
- **Pagination**: Limit queries to 500 rows for UI responsiveness
- **Aggregations**: SQL-level GROUP BY (not in-memory)

### UI Responsiveness
- **PyQtGraph**: Hardware-accelerated chart rendering
- **Lazy Loading**: Only load visible data
- **Background Tasks**: Ready for threading (future)

---

## 🎓 Learning Showcase

### Skills Demonstrated

#### Data Engineering
- ETL pipeline (Extract CSV → Transform data → Load to DB)
- Schema design with normalization
- SQL aggregations and window functions
- Data validation and error handling

#### Software Engineering
- Clean architecture (models, services, views)
- Dependency injection (session factory)
- Error handling with try/catch and rollback
- Type hints and modern Python

#### Desktop Development
- Native UI with Qt framework
- Event-driven architecture
- Custom widget composition
- Packaging and distribution

#### Domain Knowledge
- Double-entry bookkeeping
- Chart of accounts
- Reconciliation and period close
- Financial reporting

---

## 🎯 Use Cases

### Personal Finance
- Track bank accounts, credit cards
- Categorize expenses automatically
- Monitor spending by category
- Reconcile statements monthly

### Small Business
- Basic bookkeeping for sole proprietors
- Track income and expenses
- Generate cashflow reports
- Prepare for tax filing

### Learning Tool
- Understand double-entry bookkeeping
- Practice data modeling
- Explore desktop app development
- Study financial concepts

---

## 🔮 Future Enhancement Ideas

### High Priority
1. **Transfer Detection**: Match opposite transactions between accounts
2. **Budget Tracking**: Set monthly budgets, track progress
3. **Period Close**: Lock past periods to prevent edits
4. **Search**: Full-text search on descriptions
5. **Export**: CSV/PDF report generation

### Medium Priority
6. **Multi-Currency**: Exchange rates and foreign accounts
7. **Attachments**: Upload receipts, statements
8. **Recurring Transactions**: Templates for regular bills
9. **Split Transactions**: Multiple categories per transaction
10. **Tags**: Additional classification beyond categories

### Nice to Have
11. **Dark Mode**: Alternative theme
12. **Keyboard Shortcuts**: Power-user features
13. **Undo/Redo**: Command pattern for edits
14. **Backup/Restore**: Automated backups
15. **Cloud Sync**: Optional online backup

---

## 📸 Screenshot Placeholders

*(Add actual screenshots here for portfolio)*

1. **Dashboard**: Charts showing cashflow and categories
2. **Import Wizard**: CSV mapping interface
3. **Transactions**: Table with inline editing
4. **Rules Manager**: Rules list with priority
5. **Reports**: Formatted text reports

---

## 💡 Interview Talking Points

### "What makes this unique?"
> "Most finance apps are web-based or mobile. This is a desktop app with local-first data, which means no cloud dependency, instant performance, and full data privacy. It's also open-source, so users can audit the code and trust their financial data."

### "How does it handle errors?"
> "At every layer. CSV import validates dates and amounts, skipping invalid rows. The rules engine uses try/catch for regex errors. Database operations use session management with automatic rollback on exceptions. The UI provides feedback via status labels."

### "Why double-entry bookkeeping?"
> "It's the foundation of all accounting systems—banks, companies, personal finance apps. By implementing it, I demonstrate understanding of financial data models and constraints. It also ensures data integrity: every transaction must balance."

### "How would you scale this?"
> "For larger datasets, I'd add pagination to all views, not just transactions. Batch operations could move to background threads with progress bars. The database could migrate from SQLite to PostgreSQL for concurrent writes. Charts could use data sampling for 10,000+ points."

