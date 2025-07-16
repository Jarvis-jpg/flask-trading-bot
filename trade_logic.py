
import json
from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome

def process_trade(trade_data):
try:
# Validate required fields
required_fields = ["pair", "action", "entry", "stop_loss", "take_profit", "confidence", "strategy", "timestamp"]
for field in required_fields:
if field not in trade_data:
raise ValueError(f"Missing required field: {field}")

print("✅ Translated TradingView alert to internal format.")

# Predict trade outcome using AI
try:
outcome = predict_trade_outcome(trade_data)
print(f"🤖 AI prediction: {outcome}")
except Exception as e:
print(f"❌ Error predicting trade: {e}")
outcome = "unknown"

# Calculate potential profit
if trade_data["action"] == "buy":
profit = trade_data["take_profit"] - trade_data["entry"]
else:
profit = trade_data["entry"] - trade_data["take_profit"]

# Log trade
log_trade({
"pair": trade_data["pair"],
"action": trade_data["action"],
"entry": trade_data["entry"],
"stop_loss": trade_data["stop_loss"],
"take_profit": trade_data["take_profit"],
"confidence": trade_data["confidence"],
"strategy": trade_data["strategy"],
"timestamp": trade_data["timestamp"],
"ai_prediction": outcome,
"profit": round(profit, 5)
})

except Exception as e:
print(f"ERROR in process_trade: {e}")
