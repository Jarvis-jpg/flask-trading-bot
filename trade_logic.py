import json
import os
from datetime import datetime

# Path to store the journal
JOURNAL_FILE = "trade_journal.json"

# Load existing journal data or initialize empty list
def load_journal():
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save updated journal
def save_journal(journal):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(journal, file, indent=2)

# Simulate PnL calculation (you can replace with real broker logic)
def calculate_pnl(trade):
    risk = abs(trade["entry"] - trade["stop_loss"])
    reward = abs(trade["take_profit"] - trade["entry"])
    win = reward > risk  # dummy win condition
    trade["result"] = "win" if win else "loss"
    trade["pnl"] = round(reward * 100 if win else -risk * 100, 2)
    return trade

# ✅ Main entry function used in app.py
def process_trade(data):
    print(f"Processing trade: {data}")
    trade = {
        "pair": data.get("pair"),
        "action": data.get("action"),
        "entry": float(data.get("entry")),
        "stop_loss": float(data.get("stop_loss")),
        "take_profit": float(data.get("take_profit")),
        "strategy_id": data.get("strategy_id", "macd_ema_v7"),
        "confidence": float(data.get("confidence", 0)),
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat())
    }

    # Evaluate and log trade
    trade = calculate_pnl(trade)
    journal = load_journal()
    journal.append(trade)
    save_journal(journal)

    return {
        "status": "success",
        "message": "Trade processed",
        "result": trade
    }


    @staticmethod
    def log_trade(trade):
        df = pd.DataFrame([trade])
        file_exists = os.path.isfile(AdaptiveTradeLogic.journal_path)
        df.to_csv(AdaptiveTradeLogic.journal_path, mode='a', header=not file_exists, index=False)
