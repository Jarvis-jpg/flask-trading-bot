import json
from datetime import datetime
from learner import analyze_and_learn
from ai_learning import predict_trade  # ✅ Step 1: Import

def process_trade(data):
    pair = data["pair"]
    action = data["action"]
    entry = float(data["entry"])
    stop_loss = float(data["stop_loss"])
    take_profit = float(data["take_profit"])
    confidence = float(data.get("confidence", 0))
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    reward = round(abs(take_profit - entry) * 10000, 2)
    risk = round(abs(entry - stop_loss) * 10000, 2)
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
        "timestamp": timestamp,
    }

    # ✅ Step 2: Add AI confidence before saving
    predicted_win_prob = predict_trade(trade_result)
    trade_result["ai_confidence"] = round(predicted_win_prob, 2)

    try:
        with open("trade_journal.json", "r") as f:
            trades = json.load(f)
    except:
        trades = []

    trades.append(trade_result)

    with open("trade_journal.json", "w") as f:
        json.dump(trades, f, indent=2)

    try:
        analyze_and_learn()
    except:
        pass

    return trade_result



    @staticmethod
    def log_trade(trade):
        df = pd.DataFrame([trade])
        file_exists = os.path.isfile(AdaptiveTradeLogic.journal_path)
        df.to_csv(AdaptiveTradeLogic.journal_path, mode='a', header=not file_exists, index=False)
