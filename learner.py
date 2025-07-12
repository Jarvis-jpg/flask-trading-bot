import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

MODEL_PATH = "ai_model.pkl"

def load_data():
    with open("trade_journal.json", "r") as f:
        trades = json.load(f)
    return pd.DataFrame(trades)

def engineer_features(df):
    df["reward_risk"] = abs((df["take_profit"] - df["entry"]) / (df["stop_loss"] - df["entry"]))
    df["direction"] = df["action"].map({"buy": 1, "sell": -1})
    df["target"] = df["result"].map({"win": 1, "loss": 0})
    features = ["entry", "stop_loss", "take_profit", "confidence", "reward_risk", "direction"]
    return df[features], df["target"]

def train_ai():
    df = load_data()
    if len(df) < 20:
        return "Not enough trades yet to train."
    
    X, y = engineer_features(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump((model, scaler), MODEL_PATH)
    acc = model.score(X_test, y_test)
    return f"Model trained. Test accuracy: {acc:.2f}"

def predict_trade(trade):
    try:
        model, scaler = joblib.load(MODEL_PATH)
    except:
        return 0.5  # default confidence

    rr = abs((trade["take_profit"] - trade["entry"]) / (trade["stop_loss"] - trade["entry"]))
    direction = 1 if trade["action"] == "buy" else -1
    X = np.array([[trade["entry"], trade["stop_loss"], trade["take_profit"], trade["confidence"], rr, direction]])
    X_scaled = scaler.transform(X)
    return float(model.predict_proba(X_scaled)[0][1])  # probability of win
import json
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

model = None

def analyze_and_learn():
    global model
    try:
        with open("trade_journal.json", "r") as file:
            trades = json.load(file)
    except Exception as e:
        print(f"Error loading journal: {e}")
        return

    if not trades:
        print("No trades to learn from.")
        return

    df = pd.DataFrame(trades)
    df = df[df["result"].isin(["win", "loss"])]

    if df.empty:
        print("No valid win/loss trades.")
        return

    df["label"] = df["result"].map({"win": 1, "loss": 0})
    features = df[["entry", "stop_loss", "take_profit", "confidence"]]
    labels = df["label"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(features, labels)

    print("Model trained on trade history.")

