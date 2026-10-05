-- Supermarket Sales Analytics
-- PostgreSQL-style SQL. Adapt DATE functions for MySQL if needed.

-- 1. Total sales and profit
SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2) AS profit_margin_pct
FROM supermarket_sales;

-- 2. Sales by category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS units_sold
FROM supermarket_sales
GROUP BY Category
ORDER BY sales DESC;

-- 3. Branch performance
SELECT
    Branch,
    City,
    ROUND(SUM(Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit,
    COUNT(*) AS transactions
FROM supermarket_sales
GROUP BY Branch, City
ORDER BY sales DESC;

-- 4. Payment method usage
SELECT
    Payment_Method,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS sales
FROM supermarket_sales
GROUP BY Payment_Method
ORDER BY transactions DESC;

-- 5. Member vs normal customers
SELECT
    Customer_Type,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit
FROM supermarket_sales
GROUP BY Customer_Type
ORDER BY sales DESC;

-- 6. Top 10 products by sales
SELECT
    Product,
    Category,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Sales), 2) AS sales
FROM supermarket_sales
GROUP BY Product, Category
ORDER BY sales DESC
LIMIT 10;

-- 7. Monthly sales
SELECT
    EXTRACT(YEAR FROM Date) AS year,
    EXTRACT(MONTH FROM Date) AS month,
    ROUND(SUM(Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit
FROM supermarket_sales
GROUP BY year, month
ORDER BY year, month;
