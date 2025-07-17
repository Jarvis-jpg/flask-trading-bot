from datetime import datetime, timedelta, UTC
import requests
import random
import json

# Trading pairs to simulate
pairs = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "MATICUSDT"]

def generate_trade(i):
    pair = random.choice(pairs)
    action = random.choice(["buy", "sell"])
    price = round(random.uniform(100, 1000), 2)
    
    return {
        "pair": pair,
        "action": action,
        "entry": price,
        "stop_loss": round(price * 0.99, 2),
        "take_profit": round(price * 1.02, 2),
        "confidence": round(random.uniform(0.6, 0.9), 2),
        "strategy": "MACD+EMA",
        "timestamp": datetime.now(UTC).isoformat() + "Z",
        "result": random.choice(["win", "loss"]),
        "profit": round(random.uniform(-10, 20), 2)
    }

def simulate_trades(num_trades=100):
    endpoint = "http://localhost:5000/webhook"
    
    for i in range(num_trades):
        trade = generate_trade(i)
        
        try:
            response = requests.post(endpoint, json=trade)
            if response.status_code == 200:
                print(f"[✓] Trade {i+1} executed successfully")
            else:
                print(f"[✗] Trade {i+1} failed: {response.text}")
        except Exception as e:
            print(f"[✗] Error in trade {i+1}: {str(e)}")

if __name__ == "__main__":
    simulate_trades()