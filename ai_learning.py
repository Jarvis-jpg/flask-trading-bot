import json
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

def load_data():
    try:
        with open("trade_journal.json", "r") as f:
            trades = json.load(f)
    except:
        return [], []

    X, y = [], []
    for t in trades:
        features = [t["entry"], t["stop_loss"], t["take_profit"], t["confidence"]]
        X.append(features)
        y.append(1 if t["result"] == "win" else 0)
    return X, y

def train_ai():
    X, y = load_data()
    if len(X) < 10:
        return
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    joblib.dump(model, "ai_model.pkl")

def predict_trade(trade):
    try:
        model = joblib.load("ai_model.pkl")
        features = [[
            trade["entry"],
            trade["stop_loss"],
            trade["take_profit"],
            trade["confidence"]
        ]]
        return model.predict_proba(features)[0][1]  # Probability of win
    except:
        return 0.5  # Default fallback
