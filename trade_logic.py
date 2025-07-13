import json
from datetime import datetime
import pandas as pd

from learner import analyze_and_learn
from ai_learning import predict_trade, train_ai
from oanda_trade import place_order
from trade_journal import log_trade

def process_trade(data):
    try:
        pair = data["pair"]
        action = data["action"]
        entry = float(data["entry"])
        stop_loss = float(data["stop_loss"])
        take_profit = float(data["take_profit"])
        confidence = float(data.get("confidence", 0.0))
        strategy = data.get("strategy", "unknown")
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        rr_ratio = round(abs(take_profit - entry) / abs(entry - stop_loss), 2)
        win_expected = confidence >= 0.7
        result = "win" if win_expected else "loss"
        pnl = round((take_profit - entry) * 10000, 2) if win_expected else -round((entry - stop_loss) * 10000, 2)

        # Predict AI win probability
        predicted_win_prob = predict_trade({
            "pair": pair,
            "action": action,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence
        })

        trade_result = {
            "pair": pair,
            "action": action,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence,
            "strategy": strategy,
            "timestamp": timestamp,
            "ai_confidence": round(predicted_win_prob, 2),
            "result": result,
            "pnl": pnl,
            "rr": rr_ratio
        }

        log_trade(
            pair=pair,
            action=action,
            entry_price=entry,
            sl=stop_loss,
            tp=take_profit,
            result=result,
            profit=pnl,
            rr=rr_ratio,
            strategy=strategy
        )

        # Place trade with OANDA live
        units = 1000  # You can replace this with dynamic sizing
        place_order(pair, action, units, entry, stop_loss, take_profit)

        return trade_result

    except Exception as e:
        print("ERROR in process_trade:", str(e))
        return {"status": "error", "message": str(e)}
