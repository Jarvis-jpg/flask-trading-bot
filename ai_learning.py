import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

MODEL_PATH = "model.pkl"

def train_ai(trade_data):
    df = pd.DataFrame(trade_data)

    if len(df) < 10:
        return "Not enough data to train."

    df["target"] = df["profit"].apply(lambda x: 1 if x > 0 else 0)

    features = ["price", "profit"]
    X = df[features]
    y = df["target"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump((model, scaler), MODEL_PATH)
    return "AI training complete."

def predict_trade(trade):
    model_data = joblib.load(MODEL_PATH)
    model, scaler = model_data

    features = np.array([[trade["price"], trade["profit"]]])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)

    return "high_quality" if prediction[0] == 1 else "low_quality"
