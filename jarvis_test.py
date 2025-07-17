import requests
import json
from datetime import datetime, UTC
import random
import time
import os

# Trading pairs with realistic price ranges
PAIRS = {
    "BTCUSDT": {"base": 45000, "volatility": 1000},
    "ETHUSDT": {"base": 2500, "volatility": 100},
    "SOLUSDT": {"base": 100, "volatility": 5},
    "MATICUSDT": {"base": 1.5, "volatility": 0.1}
}

def get_server_url():
    """Get the server URL from environment or use default"""
    render_url = os.getenv('RENDER_URL')
    if render_url:
        return f"https://{render_url}"
    return "http://localhost:5000"

def generate_trade():
    """Generate a realistic trade with proper format"""
    pair = random.choice(list(PAIRS.keys()))
    pair_info = PAIRS[pair]
    price = round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 2)
    
    return {
        "pair": pair,
        "action": random.choice(["buy", "sell"]),
        "entry": price,
        "stop_loss": round(price * 0.99, 2),
        "take_profit": round(price * 1.02, 2),
        "confidence": round(random.uniform(0.65, 0.95), 2),
        "strategy": "MACD+EMA",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

def run_test(num_trades=100, delay=1):
    """Run trade tests against the Jarvis webhook"""
    server_url = get_server_url()
    webhook_url = f"{server_url}/webhook"
    success = 0
    failed = 0
    
    print(f"\n🤖 Jarvis Trade Test")
    print(f"📡 Server URL: {server_url}")
    print(f"🔄 Running {num_trades} test trades...\n")
    
    # Test server connection
    try:
        health = requests.get(server_url)
        if health.status_code != 200:
            print("❌ Server not responding!")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        return
    
    # Run trade tests
    start_time = time.time()
    for i in range(num_trades):
        trade = generate_trade()
        try:
            response = requests.post(webhook_url, json=trade)
            if response.status_code == 200:
                success += 1
                print(f"✅ Trade {i+1}: {trade['pair']} {trade['action']} @ {trade['entry']}")
            else:
                failed += 1
                print(f"❌ Trade {i+1} failed: {response.text}")
        except Exception as e:
            failed += 1
            print(f"❌ Error in trade {i+1}: {str(e)}")
        
        time.sleep(delay)  # Prevent overwhelming the server
    
    # Print summary
    duration = round(time.time() - start_time, 2)
    print(f"\n📊 Test Summary:")
    print(f"Total trades: {num_trades}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration}s")
    print(f"Success rate: {round((success/num_trades)*100, 2)}%")

if __name__ == "__main__":
    run_test(num_trades=10, delay=1)  # Start with 10 trades for initial testing