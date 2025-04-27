# main.py

"""
🚪 Entry Point – FastAPI App
----------------------------
Receives user questions and returns both:
1. Rule-based SQL (from ERD pattern matching)
2. LLM-generated SQL (via prompt formatting)
3. Executed results if SQL is run
"""

from fastapi import FastAPI
from pydantic import BaseModel
from controller import generate_sql_response
from run_sql import run_sql_query

# 🚀 Initialize FastAPI app
app = FastAPI()

# 📝 Request models
class QueryRequest(BaseModel):
    question: str

class RunSQLRequest(BaseModel):
    sql_query: str

# 📡 Root endpoint (health check)
@app.get("/")
def read_root():
    return {"message": "BLISS backend is up and running 🚀"}

# 📡 SQL generation endpoint
@app.post("/generate_sql")
def generate_sql(request: QueryRequest):
    return generate_sql_response(request.question)

# 📡 SQL execution endpoint
@app.post("/run_sql")
def run_sql(request: RunSQLRequest):
    return run_sql_query(request.sql_query)
