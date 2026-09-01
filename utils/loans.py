import json
import os

LOANS_FILE = "data/loans.json"

def load_loans():
    with open(LOANS_FILE, "r") as f:
        return json.load(f)

def save_loans(loans):
    tmp_path = f"{LOANS_FILE}.tmp"
    with open(tmp_path, "w") as f:
        json.dump(loans, f, indent=4)
    os.replace(tmp_path, LOANS_FILE)
