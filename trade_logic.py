# trade_logic.py

import json
from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome


def process_trade(data):
try:
pair = data["pair"]
action = data["action"]
entry = data["entry"]
stop_loss = data["stop_loss"]
take_profit = data["take_profit"]
confidence = data.get("confidence", 0.5)
strategy = data.get("strategy", "Unknown")
timestamp = data.get("timestamp", "")

# Predict outcome
prediction = predict_trade_outcome({
"pair": pair,
"entry": entry,
"stop_loss": stop_loss,
"take_profit": take_profit,
"confidence": confidence,
"strategy": strategy
})

print(f"🤖 AI prediction: {prediction}")

# Dummy profit calc (replace with real broker result logic)
profit = round((take_profit - entry) if action == "buy" else (entry - stop_loss), 5)

# Log trade
log_trade({
"pair": pair,
"action": action,
"entry": entry,
"stop_loss": stop_loss,
"take_profit": take_profit,
"confidence": confidence,
"strategy": strategy,
"timestamp": timestamp,
"result": prediction,
"profit": profit
})

except KeyError as e:
print(f"ERROR in process_trade: Missing required field: {e}")
except Exception as e:
print(f"ERROR in process_trade: {e}")

