import json
import os
from datetime import datetime

JOURNAL_FILE = "trade_journal_cleaned.json"

def initialize_journal():
    if not os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "w") as f:
            json.dump({"trades": []}, f, indent=4)

def log_trade(trade_data):
    initialize_journal()
    try:
        with open(JOURNAL_FILE, "r+") as f:
            data = json.load(f)
            trade_data["status"] = "pending"
            trade_data["profit"] = None
            trade_data["closed_at"] = None
            data["trades"].append(trade_data)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"[Logger Error] Failed to log trade: {e}")

def update_trade_result(trade_id, profit, status, exit_time=None):
    initialize_journal()
    try:
        with open(JOURNAL_FILE, "r+") as f:
            data = json.load(f)
            for trade in data["trades"]:
                if trade.get("id") == trade_id:
                    trade["status"] = status
                    trade["profit"] = profit
                    trade["closed_at"] = exit_time or datetime.now().isoformat()
                    break
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"[Journal Update Error] {e}")
