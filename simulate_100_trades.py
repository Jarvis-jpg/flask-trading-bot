from datetime import datetime, UTC
import requests
import random
import time

PAIRS = {
    "BTCUSDT": {"base": 45000, "volatility": 1000},
    "ETHUSDT": {"base": 2500, "volatility": 100},
    "SOLUSDT": {"base": 100, "volatility": 5},
    "MATICUSDT": {"base": 1.5, "volatility": 0.1}
}

def generate_realistic_price(pair_info):
    return round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 2)

def create_trade():
    pair = random.choice(list(PAIRS.keys()))
    price = generate_realistic_price(PAIRS[pair])
    sl_percent = random.uniform(0.5, 1.5) / 100  # 0.5% to 1.5% stop loss
    tp_percent = random.uniform(1, 3) / 100      # 1% to 3% take profit
    
    return {
        "pair": pair,
        "action": random.choice(["buy", "sell"]),
        "entry": price,
        "stop_loss": round(price * (1 - sl_percent), 2),
        "take_profit": round(price * (1 + tp_percent), 2),
        "confidence": round(random.uniform(0.65, 0.95), 2),
        "strategy": "MACD+EMA",
        "timestamp": datetime.now(UTC).isoformat() + "Z"
    }

def run_simulation():
    success = 0
    failed = 0
    endpoint = "http://127.0.0.1:5000/webhook"
    
    print("🤖 Starting trade simulation...")
    
    for i in range(100):
        trade = create_trade()
        try:
            response = requests.post(endpoint, json=trade)
            if response.status_code == 200:
                success += 1
                print(f"✅ Trade {i+1}: {trade['pair']} {trade['action']} @ {trade['entry']}")
            else:
                failed += 1
                print(f"❌ Trade {i+1} failed: {response.text}")
        except Exception as e:
            failed += 1
            print(f"❌ Error in trade {i+1}: {str(e)}")
        
        time.sleep(0.5)  # Delay between trades
    
    print(f"\n📊 Simulation Complete:")
    print(f"Successful trades: {success}")
    print(f"Failed trades: {failed}")

if __name__ == "__main__":
    run_simulation()