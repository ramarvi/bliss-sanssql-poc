# load_to_duckdb.py

import os
import duckdb

# ----------------------------------
# Setup paths
# ----------------------------------
DATA_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(DATA_DIR, "marketing.db")

# CSV file paths
campaign_csv = os.path.join(DATA_DIR, "dim_campaign.csv")
customer_csv = os.path.join(DATA_DIR, "dim_customer.csv")
message_csv = os.path.join(DATA_DIR, "fact_message_event.csv")

# ----------------------------------
# Connect to DuckDB
# ----------------------------------
print(f"📦 Connecting to DuckDB at {DB_PATH}")
con = duckdb.connect(DB_PATH)

# ----------------------------------
# Create tables
# ----------------------------------

print("🧱 Creating tables...")

con.execute("""
CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name TEXT,
    start_date DATE,
    end_date DATE,
    channel TEXT
)
""")

con.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    region TEXT,
    signup_date DATE
)
""")

con.execute("""
CREATE TABLE IF NOT EXISTS fact_message_event (
    message_id INTEGER PRIMARY KEY,
    campaign_id INTEGER,
    customer_id INTEGER,
    event_type TEXT,
    event_date DATE
)
""")

# ----------------------------------
# Load CSV data
# ----------------------------------

print("📥 Loading data from CSVs...")

con.execute(f"COPY dim_campaign FROM '{campaign_csv}' (HEADER, DELIMITER ',')")
print("✅ Loaded: dim_campaign")

con.execute(f"COPY dim_customer FROM '{customer_csv}' (HEADER, DELIMITER ',')")
print("✅ Loaded: dim_customer")

con.execute(f"COPY fact_message_event FROM '{message_csv}' (HEADER, DELIMITER ',')")
print("✅ Loaded: fact_message_event")

# ----------------------------------
# Wrap-up
# ----------------------------------

print("🎉 Done! Data loaded successfully into marketing.db")
