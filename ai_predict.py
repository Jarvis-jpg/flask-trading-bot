import joblib
import numpy as np

def predict_trade_outcome(trade):
try:
model = joblib.load("model.pkl")

# Extract relevant features from the trade
features = np.array([
float(trade["entry"]),
float(trade["stop_loss"]),
float(trade["take_profit"]),
float(trade["confidence"])
]).reshape(1, -1)

prediction = model.predict(features)[0]
probas = model.predict_proba(features)[0]
confidence = round(max(probas), 2)

return prediction, confidence

except Exception as e:
print(f"❌ Error predicting trade: {e}")
raise