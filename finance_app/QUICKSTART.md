# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run the App

```bash
python finance_app/main.py
```

## 3. Import Sample Data

1. Click the **Import** tab
2. Click **Browse CSV…**
3. Select `sample_data/bank_statement_1.csv`
4. Map columns:
   - Date column: `date`
   - Description column: `description`
   - Amount column: `amount`
   - Source account: `Checking`
5. Click **Import**
6. Repeat for `sample_data/bank_statement_2.csv`

## 4. Create Categorization Rules

Go to **Rules** tab and add these rules:

| Pattern | Category ID | Priority |
|---------|-------------|----------|
| `salary\|paycheck\|deposit` | 5 (Salary) | 10 |
| `grocery\|walmart\|target\|costco\|whole foods` | 1 (Groceries) | 20 |
| `rent\|landlord` | 2 (Rent) | 15 |
| `electric\|water\|internet\|comcast` | 3 (Utilities) | 25 |
| `restaurant\|chipotle\|starbucks\|coffee\|dunkin\|uber eats` | 4 (Dining) | 30 |
| `gas\|shell` | 6 (Misc) | 35 |
| `pharmacy\|cvs` | 6 (Misc) | 40 |

Then:
1. Click **Dry Run** to preview matches
2. Click **Apply Rules** to categorize transactions

## 5. Generate Double-Entry Postings

1. Go to **Reports** tab
2. Click **Generate All Postings**
3. Click **Account Balances** to see ledger balances

## 6. View Dashboard

1. Go to **Dashboard** tab
2. Select time range (Last Quarter or All Time)
3. View interactive charts:
   - Cashflow by month (income, expenses, net)
   - Top expense categories

## 7. View Reports

In the **Reports** tab, try:
- **Cashflow by Month**: See monthly income/expenses
- **Category Breakdown**: Top expense categories
- **Account Balances**: Current ledger balances
- **Reconciliation Report**: Period summary

## 8. Package as .exe (Optional)

```bash
pip install pyinstaller
pyinstaller finance_app.spec
```

Run the packaged app:
```bash
cd dist/FinanceApp
FinanceApp.exe
```

## Tips

- The database (`finance_app.db`) is created in your current directory
- Use **Transactions** tab to manually adjust categories
- **Refresh** button on Dashboard updates charts
- Rules are matched by priority (lowest first)
- Postings must be generated before viewing account balances

