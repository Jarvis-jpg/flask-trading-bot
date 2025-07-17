import requests
import json
from datetime import datetime, UTC
import random
import time
import os
import sys

# Trading pairs with realistic price ranges
PAIRS = {
    "BTCUSDT": {"base": 45000, "volatility": 1000},
    "ETHUSDT": {"base": 2500, "volatility": 100},
    "SOLUSDT": {"base": 100, "volatility": 5},
    "MATICUSDT": {"base": 1.5, "volatility": 0.1}
}

def get_server_url():
    """Get the server URL from environment or use default"""
    # Check for Render URL first
    render_url = os.getenv('RENDER_URL')
    if render_url:
        return f"https://{render_url}"
    
    # Default to localhost if no Render URL
    return "http://127.0.0.1:5000"

def generate_trade():
    """Generate a realistic trade with proper format"""
    pair = random.choice(list(PAIRS.keys()))
    pair_info = PAIRS[pair]
    price = round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 2)
    
    # Calculate stop loss and take profit based on action
    action = random.choice(["buy", "sell"])
    if action == "buy":
        stop_loss = round(price * 0.99, 2)  # 1% below entry
        take_profit = round(price * 1.02, 2)  # 2% above entry
    else:
        stop_loss = round(price * 1.01, 2)  # 1% above entry
        take_profit = round(price * 0.98, 2)  # 2% below entry
    
    return {
        "pair": pair,
        "action": action,
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": round(random.uniform(0.65, 0.95), 2),
        "strategy": "MACD+EMA",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

def test_server_connection(server_url):
    """Test server health and connectivity"""
    try:
        health = requests.get(server_url, timeout=5)
        print(f"\n🔍 Server Health Check:")
        print(f"URL: {server_url}")
        print(f"Status: {health.status_code}")
        print(f"Response: {health.text[:100]}...")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {server_url}")
        return False
    except Exception as e:
        print(f"❌ Server test failed: {str(e)}")
        return False

def run_test(num_trades=10, delay=1):
    """Run trade tests against the Jarvis webhook"""
    server_url = get_server_url()
    webhook_url = f"{server_url}/webhook"
    success = 0
    failed = 0
    
    print("\n🤖 Jarvis Trade Test")
    print(f"📡 Server URL: {server_url}")
    print(f"🔄 Running {num_trades} test trades...")
    
    # Verify server connection
    if not test_server_connection(server_url):
        return
    
    # Run trade tests
    start_time = time.time()
    for i in range(num_trades):
        trade = generate_trade()
        try:
            response = requests.post(
                webhook_url, 
                json=trade,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                success += 1
                print(f"✅ Trade {i+1}: {trade['pair']} {trade['action']} @ {trade['entry']}")
            else:
                failed += 1
                print(f"❌ Trade {i+1} failed ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            failed += 1
            print(f"❌ Network error in trade {i+1}: {str(e)}")
        except Exception as e:
            failed += 1
            print(f"❌ Error in trade {i+1}: {str(e)}")
        
        # Progress indicator
        sys.stdout.write(f"\rProgress: {i+1}/{num_trades} trades completed")
        sys.stdout.flush()
        
        time.sleep(delay)
    
    # Print summary
    duration = round(time.time() - start_time, 2)
    print(f"\n\n📊 Test Summary:")
    print(f"Total trades: {num_trades}")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration}s")
    print(f"Success rate: {round((success/num_trades)*100, 2)}%")

if __name__ == "__main__":
    try:
        num_trades = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        delay = float(sys.argv[2]) if len(sys.argv) > 2 else 1
        run_test(num_trades=num_trades, delay=delay)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {str(e)}")