import json
import os

STOCKS_FILE = "data/stocks.json"

def load_stocks():
    with open(STOCKS_FILE, "r") as f:
        return json.load(f)
    
def save_stocks(stocks):
    tmp_path = f"{STOCKS_FILE}.tmp"
    with open(tmp_path, "w") as f:
        json.dump(stocks, f, indent=4)
    os.replace(tmp_path, STOCKS_FILE)