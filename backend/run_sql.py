# run_sql.py

"""
🏃 SQL Runner – DuckDB Execution Layer
---------------------------------------
Takes validated SQL queries and runs them safely against DuckDB.
"""

import duckdb
import os

# 📂 Path to DuckDB database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "marketing.db")

# 🏃 Main function to run SQL
from sql_validator import validate_and_format_sql  # 🆕 Import

def run_sql_query(sql_query: str):
    try:
        # 🛡️ Step 1: Validate and format
        validation = validate_and_format_sql(sql_query)
        
        if not validation["success"]:
            return {"error": f"SQL Validation Failed: {validation['error']}"}
        
        formatted_sql = validation["formatted_sql"]

        # 🛡️ Step 2: Connect and Execute
        con = duckdb.connect(DB_PATH)
        result = con.execute(formatted_sql).fetchall()
        columns = [desc[0] for desc in con.description]
        
        return {
            "columns": columns,
            "rows": result
        }
    
    except Exception as e:
        return {"error": str(e)}

    finally:
        # ✅ Always close the connection
        if con:
            con.close()
