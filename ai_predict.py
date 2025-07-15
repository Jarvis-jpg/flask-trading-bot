# ai_predict.py

import pickle
import numpy as np

def predict_trade_outcome(trade):
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)

        features = np.array([
            trade["entry"],
            trade["stop_loss"],
            trade["take_profit"],
            trade["confidence"]
        ]).reshape(1, -1)

        prediction = model.predict(features)
        return prediction[0]  # e.g., "win" or "loss"
    except Exception as e:
        print(f"❌ Error predicting trade: {e}")
        return None
