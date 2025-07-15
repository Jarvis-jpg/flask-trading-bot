import json
from datetime import datetime

def log_trade(pair, action, entry, stop_loss, take_profit, result, strategy, confidence, timestamp):
    trade_data = {
        "pair": pair,
        "action": action,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "result": result,
        "strategy": strategy,
        "confidence": confidence,
        "timestamp": timestamp
    }

    try:
        with open("trade_journal.json", "r") as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = []

    journal.append(trade_data)

    with open("trade_journal.json", "w") as f:
        json.dump(journal, f, indent=2)
