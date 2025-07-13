import json
from datetime import datetime

def log_trade(pair, action, entry_price, sl, tp, result, profit, rr, strategy):
    trade = {
        "timestamp": datetime.utcnow().isoformat(),
        "pair": pair,
        "action": action,
        "entry": entry_price,
        "stop_loss": sl,
        "take_profit": tp,
        "result": result,
        "profit": profit,
        "rr": rr,
        "strategy": strategy
    }

    try:
        with open("trade_journal.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(trade)

    with open("trade_journal.json", "w") as f:
        json.dump(data, f, indent=4)
