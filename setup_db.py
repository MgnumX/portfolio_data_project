import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # 1. Customers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        country TEXT,
        signup_date DATE
    )
    ''')

    # 2. Products Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL
    )
    ''')

    # 3. Orders Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        quantity INTEGER,
        total_amount REAL,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    ''')

    # Generate synthetic data
    countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Spain', 'Mexico', 'Peru']
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys', 'Psychedelics']
    
    # Insert Customers
    for i in range(1, 101):
        signup_date = datetime.now() - timedelta(days=random.randint(10, 365))
        cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?, ?, ?, ?, ?, ?)",
                       (i, f"CustomerFirst{i}", f"CustomerLast{i}", f"user{i}@example.com", random.choice(countries), signup_date.strftime('%Y-%m-%d')))
    
    # Insert Products
    for i in range(1, 51):
        price = round(random.uniform(10.0, 500.0), 2)
        cursor.execute("INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?)",
                       (i, f"Product {i}", random.choice(categories), price))

    # Insert Orders
    cursor.execute("SELECT product_id, price FROM Products")
    products = cursor.fetchall()
    
    for i in range(1, 501):
        customer_id = random.randint(1, 100)
        product = random.choice(products)
        product_id = product[0]
        price = product[1]
        quantity = random.randint(1, 5)
        total_amount = round(price * quantity, 2)
        order_date = datetime.now() - timedelta(days=random.randint(1, 300))
        
        cursor.execute("INSERT OR IGNORE INTO Orders VALUES (?, ?, ?, ?, ?, ?)",
                       (i, customer_id, product_id, order_date.strftime('%Y-%m-%d'), quantity, total_amount))

    conn.commit()
    conn.close()
    print("Database 'ecommerce.db' created successfully with 3 tables and synthetic data.")

if __name__ == "__main__":
    create_database()
