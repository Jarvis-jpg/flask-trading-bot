import requests
import json
from datetime import datetime, UTC, timedelta
import random
import time
from tqdm import tqdm
import sys

# Test configuration
CONFIG = {
    "PAIRS": {
        "BTCUSDT": {"base": 45000, "range": (40000, 50000)},
        "ETHUSDT": {"base": 2500, "range": (2000, 3000)},
        "SOLUSDT": {"base": 100, "range": (80, 120)},
        "MATICUSDT": {"base": 1.5, "range": (1.2, 1.8)}
    },
    "DELAY": 5,  # Seconds between trades
    "TOTAL_TRADES": 8000,
    "BATCH_SIZE": 10,
    "SERVER_URL": "http://127.0.0.1:5000"
}

def generate_trade():
    """Generate a valid trade with realistic parameters"""
    pair = random.choice(list(CONFIG["PAIRS"].keys()))
    pair_data = CONFIG["PAIRS"][pair]
    
    price = round(random.uniform(pair_data["range"][0], pair_data["range"][1]), 2)
    sl_percent = random.uniform(0.01, 0.02)  # 1-2% stop loss
    tp_percent = random.uniform(0.02, 0.04)  # 2-4% take profit
    action = random.choice(["buy", "sell"])
    
    # Calculate SL/TP based on action
    if action == "buy":
        stop_loss = round(price * (1 - sl_percent), 2)
        take_profit = round(price * (1 + tp_percent), 2)
    else:
        stop_loss = round(price * (1 + sl_percent), 2)
        take_profit = round(price * (1 - tp_percent), 2)
    
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

def validate_server():
    """Validate server connection and webhook endpoint"""
    try:
        # Check main endpoint
        response = requests.get(CONFIG["SERVER_URL"])
        if response.status_code != 200:
            return False, "Server health check failed"
            
        # Test webhook with single trade
        test_trade = generate_trade()
        webhook_response = requests.post(
            f"{CONFIG['SERVER_URL']}/webhook",
            json=test_trade,
            headers={'Content-Type': 'application/json'}
        )
        if webhook_response.status_code != 200:
            return False, f"Webhook test failed: {webhook_response.text}"
            
        return True, "Server validation successful"
    except Exception as e:
        return False, f"Server connection error: {str(e)}"

def run_test():
    """Execute the 8000 trade test with progress monitoring"""
    print("\n🤖 Jarvis 8000 Trade Test")
    print(f"Server URL: {CONFIG['SERVER_URL']}")
    print(f"Total trades: {CONFIG['TOTAL_TRADES']}")
    print(f"Delay between trades: {CONFIG['DELAY']}s")
    print(f"Estimated duration: {(CONFIG['TOTAL_TRADES'] * CONFIG['DELAY']) / 3600:.1f} hours")
    
    # Validate server before starting
    valid, message = validate_server()
    if not valid:
        print(f"\n❌ Validation failed: {message}")
        return
    
    # Initialize tracking
    results = {"success": 0, "failed": 0, "errors": {}}
    
    # Confirm start
    input("\nPress Enter to start the test (Ctrl+C to stop)...")
    
    try:
        with tqdm(total=CONFIG['TOTAL_TRADES'], desc="Processing trades") as pbar:
            start_time = time.time()
            
            for i in range(CONFIG['TOTAL_TRADES']):
                trade = generate_trade()
                
                try:
                    response = requests.post(
                        f"{CONFIG['SERVER_URL']}/webhook",
                        json=trade,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        results["success"] += 1
                        pbar.set_description(f"✅ {trade['pair']} {trade['action']}")
                    else:
                        results["failed"] += 1
                        error = response.text[:50]
                        results["errors"][error] = results["errors"].get(error, 0) + 1
                        pbar.set_description(f"❌ Failed")
                
                except Exception as e:
                    results["failed"] += 1
                    error = str(e)[:50]
                    results["errors"][error] = results["errors"].get(error, 0) + 1
                
                pbar.update(1)
                time.sleep(CONFIG['DELAY'])
                
                # Show progress every 100 trades
                if (i + 1) % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"\nProgress: {i+1}/{CONFIG['TOTAL_TRADES']}")
                    print(f"Success rate: {(results['success']/(i+1)*100):.1f}%")
                    print(f"Elapsed time: {elapsed/3600:.1f} hours")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    
    finally:
        # Print final results
        total_time = time.time() - start_time
        print("\n📊 Final Results:")
        print(f"Trades completed: {results['success'] + results['failed']}")
        print(f"Successful: {results['success']}")
        print(f"Failed: {results['failed']}")
        print(f"Success rate: {(results['success']/(results['success']+results['failed'])*100):.1f}%")
        print(f"Total time: {total_time/3600:.1f} hours")
        
        if results["errors"]:
            print("\nTop errors:")
            for error, count in sorted(results["errors"].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]:
                print(f"- {error}: {count} occurrences")

if __name__ == "__main__":
    run_test()