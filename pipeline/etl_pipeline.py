import pandas as pd
import sqlite3
import os

# ------------------------
# Paths
# ------------------------
RAW_DATA = "../data/raw_sales.csv"
CLEANED_DATA = "../output/cleaned_sales.csv"
DAILY_SALES = "../output/daily_sales.csv"
TOP_PRODUCTS = "../output/sales_summary.csv"
DB_PATH = "../output/sales_data.db"
SQL_QUERIES = "../sql/analytics_queries.sql"

# ------------------------
# Step 1 - Extract
# ------------------------
def extract():
    """Load raw CSV data"""
    return pd.read_csv(RAW_DATA)

# ------------------------
# Step 2 - Validate
# ------------------------
def validate(df):
    """Clean and validate data"""
    df = df.dropna()                      # remove nulls
    df = df[df['quantity'] > 0]           # remove negative quantities
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    return df

# ------------------------
# Step 3 - Transform
# ------------------------
def transform(df):
    """Add revenue and date metrics"""
    df['revenue'] = df['quantity'] * df['price']
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    return df

# ------------------------
# Step 4 - Aggregate
# ------------------------
def aggregate(df):
    """Generate analytics tables"""
    daily_sales = df.groupby('date')['revenue'].sum().reset_index()
    top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).reset_index()
    return daily_sales, top_products

# ------------------------
# Step 5 - Output CSVs
# ------------------------
def output(df_clean, daily_sales, top_products):
    """Save CSV outputs"""
    os.makedirs("../output", exist_ok=True)
    df_clean.to_csv(CLEANED_DATA, index=False)
    daily_sales.to_csv(DAILY_SALES, index=False)
    top_products.to_csv(TOP_PRODUCTS, index=False)
    print("CSV outputs saved in 'output/' folder.")

# ------------------------
# Step 6 - Load to SQLite
# ------------------------
def load_to_sqlite(df_clean):
    """Load cleaned data into SQLite database"""
    os.makedirs("../output", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    df_clean.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Cleaned data loaded into SQLite DB at {DB_PATH}")

# ------------------------
# Step 7 - Run SQL Analytics
# ------------------------
def run_sql_queries():
    """Run analytics queries from SQL file"""
    conn = sqlite3.connect(DB_PATH)
    
    print("\n--- Top Products by Revenue ---")
    query1 = """
    SELECT product, SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC;
    """
    print(pd.read_sql_query(query1, conn))

    print("\n--- Daily Revenue ---")
    query2 = """
    SELECT date, SUM(revenue) AS daily_revenue
    FROM sales
    GROUP BY date
    ORDER BY date;
    """
    print(pd.read_sql_query(query2, conn))
    
    conn.close()

# ------------------------
# Main Function
# ------------------------
def main():
    df_raw = extract()
    df_clean = validate(df_raw)
    df_transformed = transform(df_clean)
    daily_sales, top_products = aggregate(df_transformed)
    output(df_transformed, daily_sales, top_products)
    load_to_sqlite(df_transformed)
    run_sql_queries()

# ------------------------
# Run Pipeline
# ------------------------
if __name__ == "__main__":
    main()
