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
