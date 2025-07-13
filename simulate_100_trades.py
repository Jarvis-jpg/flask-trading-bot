import requests
import random
from datetime import datetime, timedelta
import time

WEBHOOK_URL = "https://jarvis-quant-sys.onrender.com/webhook"

TICKERS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]
STRATEGIES = ["MACD+EMA", "Breakout", "Mean Reversion"]

def generate_trade(i):
    return {
        "ticker": random.choice(TICKERS),
        "side": random.choice(["buy", "sell"]),
        "price": round(random.uniform(1.0, 1.5), 4),
        "strategy": random.choice(STRATEGIES),
        "time": (datetime.utcnow() + timedelta(minutes=i)).isoformat() + "Z"
    }

def send_trade(trade_data, i):
    try:
        response = requests.post(WEBHOOK_URL, json=trade_data, timeout=10)
        if response.status_code == 200:
            print(f"[✓] Trade {i+1} success: {response.json()}")
        else:
            print(f"[✗] Trade {i+1} failed: {response.text}")
    except Exception as e:
        print(f"[!] Trade {i+1} exception: {str(e)}")

def main():
    for i in range(100):
        trade = generate_trade(i)
        send_trade(trade, i)
        time.sleep(0.5)  # avoid overloading the server

if __name__ == "__main__":
    main()
