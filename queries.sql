-- 1. Total Revenue per Country (Window Function & Aggregation)
SELECT 
    c.country, 
    SUM(o.total_amount) as total_revenue,
    RANK() OVER(ORDER BY SUM(o.total_amount) DESC) as revenue_rank
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.country;

-- 2. Customer Lifetime Value (CLV) - Top 10 Customers
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as clv
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY clv DESC
LIMIT 10;

-- 3. Monthly Sales Trend (CTE)
WITH MonthlySales AS (
    SELECT 
        STRFTIME('%Y-%m', order_date) as month,
        SUM(total_amount) as monthly_revenue
    FROM Orders
    GROUP BY month
)
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
    ROUND(((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) / LAG(monthly_revenue) OVER (ORDER BY month)) * 100, 2) as growth_rate
FROM MonthlySales;

-- 4. Most Popular Product Categories
SELECT 
    p.category,
    COUNT(o.order_id) as units_sold,
    SUM(o.total_amount) as category_revenue
FROM Products p
JOIN Orders o ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- 5. Customers who haven't ordered in the last 6 months (Anti-Join/Subquery)
SELECT 
    c.customer_id, 
    c.first_name, 
    c.email,
    MAX(o.order_date) as last_order_date
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING last_order_date < DATE('now', '-6 month') OR last_order_date IS NULL;
