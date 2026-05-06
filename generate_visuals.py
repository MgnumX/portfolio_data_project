import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create assets directory
os.makedirs('assets', exist_ok=True)

# Connect to DB
conn = sqlite3.connect('ecommerce.db')

# Aesthetic setup: Psychedelic Dark Mode
plt.style.use('dark_background')

# 1. Revenue by Category
query = """
SELECT p.category, SUM(o.total_amount) as revenue
FROM Products p
JOIN Orders o ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY revenue DESC
"""
df_cat = pd.read_sql_query(query, conn)

plt.figure(figsize=(10, 6), facecolor='#0d1117')
ax = plt.axes()
ax.set_facecolor('#0d1117')
sns.barplot(data=df_cat, x='category', y='revenue', palette='plasma')
plt.title('Total Revenue by Product Category', fontsize=16, color='white', pad=20)
plt.xlabel('Category', color='gray')
plt.ylabel('Revenue ($)', color='gray')
plt.xticks(rotation=45, color='lightgray')
plt.yticks(color='lightgray')
plt.tight_layout()
plt.savefig('assets/revenue_by_category.png', dpi=300, facecolor='#0d1117')
plt.close()

# 2. Monthly Sales Trend
query2 = """
WITH MonthlySales AS (
    SELECT STRFTIME('%Y-%m', order_date) as month, SUM(total_amount) as monthly_revenue
    FROM Orders GROUP BY month
)
SELECT * FROM MonthlySales ORDER BY month
"""
df_trend = pd.read_sql_query(query2, conn)

plt.figure(figsize=(12, 6), facecolor='#0d1117')
ax = plt.axes()
ax.set_facecolor('#0d1117')
sns.lineplot(data=df_trend, x='month', y='monthly_revenue', marker='o', color='#00FFCC', linewidth=2.5)
plt.fill_between(df_trend['month'], df_trend['monthly_revenue'], color='#00FFCC', alpha=0.15)
plt.title('Monthly Sales Trend', fontsize=16, color='white', pad=20)
plt.xlabel('Month', color='gray')
plt.ylabel('Revenue ($)', color='gray')
plt.xticks(rotation=45, color='lightgray')
plt.yticks(color='lightgray')
plt.grid(color='#333333', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('assets/monthly_trend.png', dpi=300, facecolor='#0d1117')
plt.close()

conn.close()
