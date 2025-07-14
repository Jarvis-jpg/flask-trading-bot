# utils
import json
from datetime import datetime

JOURNAL_FILE = "trade_journal.json"

def log_trade(pair, action, entry, stop_loss, take_profit, confidence, result, profit, strategy, timestamp=None):
    trade_data = {
        "pair": pair,
        "action": action,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "result": result,
        "profit": profit,
        "strategy": strategy,
        "timestamp": timestamp or datetime.utcnow().isoformat()
    }

    try:
        with open(JOURNAL_FILE, "r") as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = []

    journal.append(trade_data)

    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=4)
