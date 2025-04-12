# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from controller import generate_sql_response

# 🎬 FastAPI app initialization
app = FastAPI()

# 🧾 Define the expected input format
class QueryRequest(BaseModel):
    question: str

# 📤 Endpoint to generate SQL from a natural language question
@app.post("/generate_sql")
def generate_sql(request: QueryRequest):
    return generate_sql_response(request.question)
