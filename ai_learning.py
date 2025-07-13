import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Paths
TRADE_LOG_FILE = "trade_log.json"
MODEL_FILE = "ai_model.pkl"

def load_trade_data():
    if not os.path.exists(TRADE_LOG_FILE):
        print("No trade_log.json found.")
        return None

    with open(TRADE_LOG_FILE, "r") as f:
        trades = json.load(f)

    if not trades or not isinstance(trades, list):
        print("Trade log is empty or invalid.")
        return None

    return pd.DataFrame(trades)

def preprocess_data(df):
    required_columns = {"price", "side", "strategy", "time", "outcome"}
    if not required_columns.issubset(df.columns):
        print(f"Missing required fields in trade log. Found: {df.columns.tolist()}")
        return None, None

    df["side"] = df["side"].map({"buy": 1, "sell": 0})
    df["strategy"] = df["strategy"].astype("category").cat.codes
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df["hour"] = df["time"].dt.hour
    df = df.dropna()

    X = df[["price", "side", "strategy", "hour"]]
    y = df["outcome"].astype(int)

    return X, y

def train_and_save_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("\n=== AI Training Report ===")
    print(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_FILE)
    print(f"✅ Model saved to {MODEL_FILE}")

def main():
    df = load_trade_data()
    if df is None:
        return

    X, y = preprocess_data(df)
    if X is None or y is None:
        return

    train_and_save_model(X, y)

if __name__ == "__main__":
    main()
# --- Prediction Function for Live Use ---
def predict_trade(trade):
    try:
        model = joblib.load(MODEL_FILE)

        price = float(trade.get("price", 0))
        side = 1 if trade.get("side") == "buy" else 0
        strategy = pd.Series([trade.get("strategy", "")]).astype("category").cat.codes[0]
        hour = pd.to_datetime(trade.get("time")).hour

        features = [[price, side, strategy, hour]]
        prediction = model.predict(features)[0]

        return prediction  # 1 = good trade, 0 = bad trade
    except Exception as e:
        print("AI prediction error:", e)
        return 1  # Default to allowing the trade
