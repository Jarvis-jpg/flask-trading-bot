import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Example dummy trade data
data = {
    'confidence': [0.65, 0.8, 0.72, 0.6, 0.9, 0.75, 0.85, 0.7, 0.95, 0.6],
    'reward': [20, 40, 35, 15, 50, 45, 60, 25, 70, 10],
    'risk': [10, 20, 15, 8, 25, 22, 30, 12, 35, 5],
    'result': ['win', 'win', 'win', 'loss', 'win', 'win', 'win', 'loss', 'win', 'loss']
}

df = pd.DataFrame(data)
df['result'] = df['result'].apply(lambda x: 1 if x == 'win' else 0)

X = df[['confidence', 'reward', 'risk']]
y = df['result']

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save model
joblib.dump(model, 'model.pkl')
print("✅ model.pkl created and saved.")
