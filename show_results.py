import sqlite3
import pandas as pd

conn = sqlite3.connect('ecommerce.db')

with open('queries.sql', 'r') as f:
    sql_script = f.read()

queries = sql_script.split(';')

for i, query in enumerate(queries):
    if query.strip():
        # Get the comment above the query for the title
        lines = query.strip().split('\n')
        title = lines[0] if lines[0].startswith('--') else f"Query {i+1}"
        print(f"\n{'='*50}\n{title}\n{'='*50}")
        try:
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Error executing query: {e}")

conn.close()
