import numpy as np
import pandas as pd
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

class AdaptiveTradeLogic:
    def __init__(self):
        self.model_path = "trained_model.pkl"
        self.model = self.load_or_train_model()
        self.trade_log_path = "trade_log.csv"
        self.initialize_trade_log()

    def initialize_trade_log(self):
        if not os.path.exists(self.trade_log_path):
            df = pd.DataFrame(columns=['pair', 'price', 'signal', 'result'])
            df.to_csv(self.trade_log_path, index=False)

    def log_trade(self, pair, price, signal, result):
        df = pd.read_csv(self.trade_log_path)
        df.loc[len(df)] = [pair, price, signal, result]
        df.to_csv(self.trade_log_path, index=False)

    def load_or_train_model(self):
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)
        else:
            return self.train_model()

    def train_model(self):
        # Generate synthetic training data
        np.random.seed(42)
        data = pd.DataFrame({
            'macd': np.random.randn(500),
            'macd_signal': np.random.randn(500),
            'ema': np.random.randn(500),
            'bb_high': np.random.randn(500),
            'bb_low': np.random.randn(500),
            'label': np.random.randint(0, 2, 500)  # 0 = no trade, 1 = good trade
        })

        X = data.drop("label", axis=1)
        y = data["label"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"Model trained with accuracy: {acc:.2f}")

        joblib.dump(model, self.model_path)
        return model

    def extract_features(self, df):
        df = df.copy()
        macd = MACD(close=df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['ema'] = EMAIndicator(close=df['close']).ema_indicator()
        bb = BollingerBands(close=df['close'])
        df['bb_high'] = bb.bollinger_hband()
        df['bb_low'] = bb.bollinger_lband()
        df = df.dropna()
        return df

    def evaluate_trade(self, df):
        df = self.extract_features(df)
        latest = df.iloc[-1][['macd', 'macd_signal', 'ema', 'bb_high', 'bb_low']].values.reshape(1, -1)
        prediction = self.model.predict(latest)
        return prediction[0] == 1
