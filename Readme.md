# Batch Sales Data Pipeline for Analytics

A **professional-grade ETL pipeline** that simulates real-world batch data workflows for sales analytics.

This project processes raw sales data, validates and transforms it, aggregates key revenue metrics, and stores results in both **CSV files** and a **SQLite database** ready for SQL analysis.

---

## 💡 Why This Project Matters

* Shows **end-to-end data engineering skills**: ETL, transformation, aggregation, and SQL analytics.
* Uses **Python and Pandas**, simulating industry-standard batch workflows.
* Includes a **SQLite database** for interactive reporting, demonstrating data warehouse concepts.
* Clean, modular structure — ready to share on GitHub or include in your portfolio.

---

## 🗂 Project Structure

```
sales-data-pipeline/
│
├── data/                  # Raw sales CSV
│   └── raw_sales.csv
│
├── output/                # Processed data outputs
│   ├── cleaned_sales.csv
│   ├── daily_sales.csv
│   ├── sales_summary.csv
│   └── sales_data.db      # SQLite database
│
├── pipeline/              # ETL pipeline script
│   └── etl_pipeline.py
│
├── sql/                   # SQL queries for analytics
│   └── analytics_queries.sql
│
└── README.md              # Project documentation
```

---

## ⚙ How to Run

1. **Install Python 3** (if not already installed).
2. Install Pandas:

```bash
pip install pandas
```

3. Run the ETL pipeline:

```bash
python pipeline/etl_pipeline.py
```

4. **Check outputs** in the `output/` folder:

   * `cleaned_sales.csv` → cleaned and transformed sales data
   * `daily_sales.csv` → daily revenue metrics
   * `sales_summary.csv` → total revenue per product
   * `sales_data.db` → SQLite database for SQL queries

5. Optional: Open `sales_data.db` with **DB Browser for SQLite** for interactive analysis:

[https://sqlitebrowser.org/](https://sqlitebrowser.org/)

---

## 📊 SQL Analytics

Use these queries in `sql/analytics_queries.sql`:

```sql
-- Total revenue by product
SELECT product, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

-- Daily revenue
SELECT date, SUM(revenue) AS daily_revenue
FROM sales
GROUP BY date
ORDER BY date;
```

---

## ✅ Skills Demonstrated

* ETL pipeline design with **Python and Pandas**
* Data validation and transformation
* Aggregation and analytics
* SQL database integration (SQLite)
* Modular, production-style project structure
* Hands-on experience with batch data workflows
