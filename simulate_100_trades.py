import requests
import random
import time
from datetime import datetime, timedelta

URL = "https://jarvis-quant-sys.onrender.com/webhook"

tickers = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
strategies = ["MACD+EMA", "RSI+Trend", "Breakout", "Pullback"]

def generate_trade(i):
    return {
        "ticker": random.choice(tickers),
        "side": random.choice(["buy", "sell"]),
        "price": round(random.uniform(1.1000, 1.3000), 4),
        "strategy": random.choice(strategies),
        "time": (datetime.utcnow() + timedelta(minutes=i)).isoformat() + "Z"
    }

success = 0
fail = 0

for i in range(100):
    trade = generate_trade(i)
    try:
        response = requests.post(URL, json=trade)
        if response.status_code == 200:
            print(f"[✓] Trade {i+1} sent: {trade['ticker']} {trade['side']} at {trade['price']}")
            success += 1
        else:
            print(f"[✗] Trade {i+1} failed: {response.text}")
            fail += 1
    except Exception as e:
        print(f"[!] Error on trade {i+1}: {e}")
        fail += 1

    time.sleep(0.25)  # Slight delay to avoid spam-blocking

print(f"\n✅ Complete: {success} trades sent successfully, {fail} failed.")
