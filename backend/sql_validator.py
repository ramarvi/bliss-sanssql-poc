# 📄 sql_validator.py
# Lightweight SQL validation, formatting, and dialect correction

import sqlglot
from sqlglot import parse_one, transpile, errors

def validate_and_format_sql(sql_query: str) -> dict:
    """
    Validate, format, and optionally transpile SQL to DuckDB dialect.
    
    Returns:
        {
            "success": bool,
            "formatted_sql": str (if success),
            "error": str (if failure)
        }
    """
    try:
        # 1. Parse the SQL (catch obvious syntax errors)
        parsed = parse_one(sql_query)
        
        # 2. Optional: transpile/correct to DuckDB dialect
        transpiled = transpile(sql_query, read="mysql", write="duckdb")
        
        # 3. Format nicely
        formatted_sql = sqlglot.transpile(
            transpiled[0], 
            read="duckdb", 
            write="duckdb", 
            pretty=True
        )[0]

        return {
            "success": True,
            "formatted_sql": formatted_sql
        }
    
    except errors.ParseError as e:
        return {
            "success": False,
            "error": f"ParseError: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unknown Error: {str(e)}"
        }
