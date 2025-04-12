# main.py

"""
🚪 Entry Point – FastAPI App
----------------------------
Receives user questions and returns both:
1. Rule-based SQL (from ERD pattern matching)
2. LLM-generated SQL (via prompt formatting)
"""

from fastapi import FastAPI
from pydantic import BaseModel
from controller import generate_sql_response

# 🚀 Initialize FastAPI app
app = FastAPI()

# 📝 Request model
class QueryRequest(BaseModel):
    question: str

# 📡 Endpoint for SQL generation
@app.get("/")
def read_root():
    return {"message": "BLISS backend is up and running 🚀"}

# SQL generation endpoint (main POC endpoint)
@app.post("/generate_sql")
def generate_sql(request: QueryRequest):
    return generate_sql_response(request.question)
