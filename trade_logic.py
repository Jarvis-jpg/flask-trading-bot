# trade_logic.py

import json
from ai_predict import predict_trade_outcome
from utils.journal_logger import log_trade

def process_trade(data):
try:
if not all(k in data for k in ("pair", "action", "entry", "stop_loss", "take_profit", "timestamp", "strategy", "confidence")):
raise ValueError("Missing required field(s)")

print("✅ Translated TradingView alert to internal format.")

predicted = predict_trade_outcome(data)
print("📊 AI Confidence:", predicted)

profit = round(data["take_profit"] - data["entry"], 5) if data["action"] == "buy" else round(data["entry"] - data["take_profit"], 5)
log_trade({
"pair": data["pair"],
"action": data["action"],
"entry": data["entry"],
"stop_loss": data["stop_loss"],
"take_profit": data["take_profit"],
"timestamp": data["timestamp"],
"strategy": data["strategy"],
"confidence": data["confidence"],
"profit": profit,
"result": "pending"
})

return "✅ Trade processed and logged."
except Exception as e:
print("ERROR in process_trade:", e)
raise
