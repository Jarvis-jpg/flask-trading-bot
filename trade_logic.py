# trade_logic.py# trade_logic.py
import json
from datetime import datetime
from utils.journal_logger import log_trade
from ai_learning import predict_trade
from oanda_trade import place_order
import os


def process_trade(data):
    try:
        required_keys = ["pair", "action", "entry", "stop_loss", "take_profit", "confidence", "strategy"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required field: {key}")

        pair = data["pair"]
        action = data["action"]
        entry = float(data["entry"])
        stop_loss = float(data["stop_loss"])
        take_profit = float(data["take_profit"])
        confidence = float(data["confidence"])
        strategy = data["strategy"]
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        predicted_win_prob = predict_trade({
            "pair": pair,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence
        })

        log_trade(
            pair=pair,
            action=action,
            entry_price=entry,
            sl=stop_loss,
            tp=take_profit,
            result="pending",
            profit=0,
            rr=2.0,
            strategy=strategy,
            ai_confidence=round(predicted_win_prob, 2),
            timestamp=timestamp
        )

        place_order(pair, action, entry, stop_loss, take_profit)

    except Exception as e:
        print(f"ERROR in process_trade: {e}")
