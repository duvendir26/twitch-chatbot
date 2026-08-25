import json

STOCKS_FILE = "data/stocks.json"

def load_stocks():
    with open(STOCKS_FILE, "r") as f:
        return json.load(f)
    
def save_stocks(stocks):
    with open(STOCKS_FILE, "w") as f:
        json.dump(stocks, f, indent=4)