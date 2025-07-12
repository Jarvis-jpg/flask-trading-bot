import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_ai():
    try:
        df = pd.read_csv("trade_history.csv")

        if len(df) < 50:
            return "Not enough trade data to train."

        df["label"] = df["result"].apply(lambda r: 1 if r == "win" else 0)
        X = df[["confidence", "entry", "stop_loss", "take_profit"]]
        y = df["label"]

        model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        model.fit(X, y)
        joblib.dump(model, "ai_model.pkl")

        return f"AI model trained on {len(df)} trades."
    except Exception as e:
        return f"Training failed: {str(e)}"

def predict_trade(trade):
    try:
        model = joblib.load("ai_model.pkl")
        X = [[
            trade.get("confidence", 0),
            trade["entry"],
            trade["stop_loss"],
            trade["take_profit"]
        ]]
        prob = model.predict_proba(X)[0][1]
        return round(prob, 2)
    except Exception as e:
        return 0.5  # Neutral confidence if model isn't ready
