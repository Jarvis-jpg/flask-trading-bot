import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
import joblib

def analyze_and_learn():
    try:
        with open("trade_journal.json", "r") as f:
            trades = json.load(f)
    except FileNotFoundError:
        print("❌ No trade journal found.")
        return

    if len(trades) < 10:
        print(f"⚠️ Not enough data to train. Only {len(trades)} trades found.")
        return

    df = pd.DataFrame(trades)

    if 'result' not in df or 'confidence' not in df:
        print("❌ Required fields missing in journal.")
        return

    df['label'] = df['result'].apply(lambda x: 1 if x == 'win' else 0)

    features = df[['confidence']]
    labels = df['label']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)

    joblib.dump(model, "model.pkl")
    print("✅ AI model trained and saved as model.pkl")

if __name__ == "__main__":
    print("📊 Training AI model from trade_journal.json...")
    analyze_and_learn()
