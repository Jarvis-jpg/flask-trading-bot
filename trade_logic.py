import json
from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome

def process_trade(data):
    try:
        print("Received webhook data:", data)

        # ✅ Validate required fields or translate if needed
        if "pair" not in data and "ticker" in data:
            print("✅ Translated TradingView alert to internal format.")
            data = {
                "pair": data["ticker"],
                "action": data["side"],
                "entry": data["price"],
                "stop_loss": round(data["price"] - 0.0025, 5),  # Adjustable logic
                "take_profit": round(data["price"] + 0.0050, 5),  # Adjustable logic
                "confidence": 0.7,
                "strategy": data.get("strategy", "unknown"),
                "timestamp": data.get("time")
            }

        required_fields = ["pair", "action", "entry", "stop_loss", "take_profit", "confidence", "strategy", "timestamp"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # ✅ Predict outcome
        try:
            predicted_result = predict_trade_outcome(data)
        except Exception as e:
            print(f"❌ Error predicting trade: {e}")
            predicted_result = "unknown"

        # ✅ Log trade
        log_trade(
            pair=data["pair"],
            action=data["action"],
            entry=data["entry"],
            stop_loss=data["stop_loss"],
            take_profit=data["take_profit"],
            confidence=data["confidence"],
            strategy=data["strategy"],
            timestamp=data["timestamp"],
            result=predicted_result
        )

        print("✅ Trade processed and logged.")
        return {"status": "success", "message": "Trade processed"}
    
    except Exception as e:
        print("ERROR in process_trade:", e)
        return {"status": "error", "message": str(e)}

