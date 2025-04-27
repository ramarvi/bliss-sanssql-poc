# test_duckdb_query.py

import os
import duckdb

# Path to the DuckDB file
DATA_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(DATA_DIR, "marketing.db")

# Connect to DuckDB
con = duckdb.connect(DB_PATH)

# Example test query: Count messages per campaign
query = """
SELECT 
    c.campaign_name,
    COUNT(m.message_id) AS message_count
FROM fact_message_event m
JOIN dim_campaign c ON m.campaign_id = c.campaign_id
GROUP BY c.campaign_name
ORDER BY message_count DESC
"""

print("🔍 Running test query...")
result = con.execute(query).fetchall()

print("\n📊 Message count by campaign:")
for row in result:
    print(f"- {row[0]}: {row[1]} messages")

con.close()
