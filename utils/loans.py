import json

LOANS_FILE = "data/loans.json"

def load_loans():
    with open(LOANS_FILE, "r") as f:
        return json.load(f)

def save_loans(loans):
    with open(LOANS_FILE, "w") as f:
        json.dump(loans, f, indent=4)
