
import json
from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome

def process_trade(trade_data):
try:
print(f"✅ Received webhook data: {trade_data}")

# Validate required fields
required_fields = ["pair", "action", "entry", "stop_loss", "take_profit", "confidence", "strategy", "timestamp"]
for field in required_fields:
if field not in trade_data:
raise ValueError(f"Missing required field: {field}")

# Predict trade outcome using AI model
predicted_result, confidence_score = predict_trade_outcome(trade_data)
print(f"🤖 AI Prediction: {predicted_result} with confidence {confidence_score}")

# Calculate profit estimate based on action
entry = float(trade_data["entry"])
stop_loss = float(trade_data["stop_loss"])
take_profit = float(trade_data["take_profit"])
action = trade_data["action"]

if action == "buy":
profit = take_profit - entry
elif action == "sell":
profit = entry - take_profit
else:
raise ValueError("Invalid action value in trade data")

# Log the trade
log_trade(
pair=trade_data["pair"],
action=action,
entry=entry,
stop_loss=stop_loss,
take_profit=take_profit,
confidence=float(trade_data["confidence"]),
strategy=trade_data["strategy"],
timestamp=trade_data["timestamp"],
result=predicted_result,
profit=round(profit, 5)
)

return {
"status": "success",
"prediction": predicted_result,
"confidence": confidence_score
}

except Exception as e:
print(f"❌ ERROR in process_trade: {e}")
return {"status": "error", "message": str(e)}
