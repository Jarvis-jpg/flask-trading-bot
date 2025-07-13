import json
import os
from datetime import datetime
import pandas as pd
from learner import analyze_and_learn
from ai_learning import predict_trade, train_ai

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

    journal_file = "trade_journal.json"
    if os.path.exists(journal_file):
        with open(journal_file, "r") as f:
            trades = json.load(f)
    else:
        trades = []

    trades.append(trade)

    with open(journal_file, "w") as f:
        json.dump(trades, f, indent=2)


def process_trade(data):
    pair = data["pair"]
    action = data["action"]
    entry = float(data["entry"])
    stop_loss = float(data["stop_loss"])
    take_profit = float(data["take_profit"])
    confidence = float(data.get("confidence", 0))
    strategy = data.get("strategy", "unknown")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    reward = round(abs(take_profit - entry) * 10000, 2)
    risk = round(abs(entry - stop_loss) * 10000, 2)
    rr = reward / risk if risk != 0 else 0

    win = confidence >= 0.7
    result = "win" if win else "loss"
    pnl = reward if win else -risk

    trade_result = {
        "pair": pair,
        "action": action,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "result": result,
        "pnl": pnl,
        "rr": rr,
        "strategy": strategy,
        "timestamp": timestamp,
    }

    # Predict AI confidence and update result
    predicted_win_prob = predict_trade(trade_result)
    trade_result["ai_confidence"] = round(predicted_win_prob, 2)

    # Log to journal
    log_trade(
        pair=pair,
        action=action,
        entry_price=entry,
        sl=stop_loss,
        tp=take_profit,
        result=result,
        profit=pnl,
        rr=rr,
        strategy=strategy
    )

    # Save trade to JSON journal (redundant if above works, but optional)
    journal_file = "trade_journal.json"
    if os.path.exists(journal_file):
        with open(journal_file, "r") as f:
            trades = json.load(f)
    else:
        trades = []

    trades.append(trade_result)
    with open(journal_file, "w") as f:
        json.dump(trades, f, indent=2)

    # Optionally trigger AI learning
    analyze_and_learn()
