# 📄 feedback_logger.py
# Lightweight feedback saving module

import os
import csv
from datetime import datetime

# 📂 Ensure metadata/feedback/ directory exists
FEEDBACK_DIR = os.path.join(os.path.dirname(__file__), "..", "metadata", "feedback")
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# 📄 Feedback file path
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "user_feedback.csv")

def save_feedback(question: str, generated_sql: str, feedback: str, thumbs: str):
    """
    Save user feedback into a CSV file under metadata/feedback/user_feedback.csv
    """
    timestamp = datetime.now().isoformat()

    # Prepare feedback row
    row = {
        "timestamp": timestamp,
        "question": question,
        "generated_sql": generated_sql,
        "feedback_text": feedback,
        "thumbs": thumbs
    }

    # Check if file exists to decide header writing
    file_exists = os.path.isfile(FEEDBACK_FILE)

    # Append feedback
    with open(FEEDBACK_FILE, mode="a", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "question", "generated_sql", "feedback_text", "thumbs"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"✅ Feedback saved: {row}")
