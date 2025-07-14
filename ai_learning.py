import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

MODEL_PATH = "model.pkl"
JOURNAL_FILE = "trade_journal.json"

def train_ai():
    try:
        df = pd.read_json(JOURNAL_FILE)
        if len(df) < 10:
            print("Not enough data to train.")
            return

        df["result"] = df["result"].map({"win": 1, "loss": 0})
        X = df[["entry", "stop_loss", "take_profit", "confidence"]]
        y = df["result"]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        print("✅ AI model trained and saved.")
    except Exception as e:
        print(f"❌ Error training AI: {e}")

def predict_trade(trade):
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        X = pd.DataFrame([{
            "entry": trade["entry"],
            "stop_loss": trade["stop_loss"],
            "take_profit": trade["take_profit"],
            "confidence": trade["confidence"]
        }])
        prediction = model.predict_proba(X)[0][1]
        return round(prediction, 2)
    except Exception as e:
        print(f"❌ Error predicting trade: {e}")
        return 0.5  # neutral confidence
