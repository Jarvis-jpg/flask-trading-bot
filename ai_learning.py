import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import json
import uuid
from ai_predict import predict_trade_outcome
from utils.journal_logger import log_trade, update_trade_result

TRADE_JOURNAL_FILE = "trade_journal.json"

def analyze_and_learn():
    try:
        print("📊 Training AI model from trade_journal.json...")

        # Load trades from journal
        with open(TRADE_JOURNAL_FILE, "r", encoding="utf-8") as f:
            trades = json.load(f)

        for trade in trades:
            # Skip if already evaluated
            if trade.get("result") in ["won", "lost"]:
                continue

            # AI prediction
            predicted_result, confidence_score = predict_trade_outcome(trade)

            # Determine actual result and profit
            entry = float(trade["entry"])
            stop_loss = float(trade["stop_loss"])
            take_profit = float(trade["take_profit"])
            action = trade["action"]

            if action == "buy":
                result = "won" if take_profit > entry else "lost"
                profit = take_profit - entry if result == "won" else stop_loss - entry
            elif action == "sell":
                result = "won" if take_profit < entry else "lost"
                profit = entry - take_profit if result == "won" else entry - stop_loss
            else:
                result = "lost"
                profit = 0.0

            # Finalize the trade in journal
            update_trade_result(
                trade_id=trade["id"],
                profit=round(profit, 5),
                status=result
            )

        print("✅ AI learning complete and journal updated.")

    except Exception as e:
        print(f"❌ Error in AI learning: {e}")

if __name__ == "__main__":
    analyze_and_learn()
