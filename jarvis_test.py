import requests
import json
from datetime import datetime, UTC, timedelta
import random
import time
import os
import sys
from tqdm import tqdm
import pandas as pd

# Trading pairs with realistic price ranges and volatility patterns
PAIRS = {
    "BTCUSDT": {"base": 45000, "volatility": 1000, "min_move": 0.5},
    "ETHUSDT": {"base": 2500, "volatility": 100, "min_move": 0.1},
    "SOLUSDT": {"base": 100, "volatility": 5, "min_move": 0.01},
    "MATICUSDT": {"base": 1.5, "volatility": 0.1, "min_move": 0.001},
    "DOGEUSDT": {"base": 0.1, "volatility": 0.01, "min_move": 0.00001}
}

def generate_trade(timestamp=None):
    """Generate realistic trade data with price action patterns"""
    pair = random.choice(list(PAIRS.keys()))
    pair_info = PAIRS[pair]
    
    # Generate price with minimal movement consideration
    price = round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 6)
    price = round(price / pair_info["min_move"]) * pair_info["min_move"]
    
    action = random.choice(["buy", "sell"])
    confidence = round(random.uniform(0.65, 0.95), 2)
    
    # Risk management: 1-2% stop loss, 2-4% take profit
    sl_percent = random.uniform(0.01, 0.02)
    tp_percent = random.uniform(0.02, 0.04)
    
    if action == "buy":
        stop_loss = round(price * (1 - sl_percent), 6)
        take_profit = round(price * (1 + tp_percent), 6)
    else:
        stop_loss = round(price * (1 + sl_percent), 6)
        take_profit = round(price * (1 - tp_percent), 6)
    
    if timestamp is None:
        timestamp = datetime.now(UTC)
    
    return {
        "pair": pair,
        "action": action,
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "strategy": "MACD+EMA",
        "timestamp": timestamp.isoformat().replace('+00:00', 'Z')
    }

def run_load_test(total_trades=8000, batch_size=100, delay=5.0):
    """Run large-scale trade testing with batching and monitoring"""
    server_url = "http://127.0.0.1:5000"
    webhook_url = f"{server_url}/webhook"
    
    results = {
        "success": 0,
        "failed": 0,
        "errors": {},
        "response_times": []
    }
    
    print(f"\n🚀 Starting Jarvis Load Test")
    print(f"📊 Configuration:")
    print(f"  - Total trades: {total_trades}")
    print(f"  - Batch size: {batch_size}")
    print(f"  - Delay between trades: {delay}s")
    
    # Test server connection
    try:
        health = requests.get(server_url, timeout=5)
        if health.status_code != 200:
            print("❌ Server health check failed!")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        return

    start_time = time.time()
    progress_bar = tqdm(total=total_trades, desc="Processing trades")

    try:
        for i in range(0, total_trades, batch_size):
            batch_start = time.time()
            batch = []
            
            # Generate batch of trades
            current_time = datetime.now(UTC)
            for j in range(min(batch_size, total_trades - i)):
                trade_time = current_time + timedelta(seconds=j)
                batch.append(generate_trade(trade_time))
            
            # Process batch
            for trade in batch:
                try:
                    request_start = time.time()
                    response = requests.post(
                        webhook_url,
                        json=trade,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    response_time = time.time() - request_start
                    results["response_times"].append(response_time)
                    
                    if response.status_code == 200:
                        results["success"] += 1
                    else:
                        results["failed"] += 1
                        error_msg = str(response.text)[:100]
                        results["errors"][error_msg] = results["errors"].get(error_msg, 0) + 1
                
                except Exception as e:
                    results["failed"] += 1
                    error_msg = str(e)[:100]
                    results["errors"][error_msg] = results["errors"].get(error_msg, 0) + 1
                
                progress_bar.update(1)
                time.sleep(delay)
            
            # Batch timing
            batch_time = time.time() - batch_start
            if batch_time < 1:  # Ensure minimum 1 second between batches
                time.sleep(1 - batch_time)
    
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    finally:
        progress_bar.close()
        total_time = time.time() - start_time
        
        # Generate report
        print("\n📈 Test Results:")
        print(f"Total trades processed: {results['success'] + results['failed']}")
        print(f"Successful trades: {results['success']}")
        print(f"Failed trades: {results['failed']}")
        print(f"Success rate: {(results['success']/(total_trades)*100):.2f}%")
        print(f"Total time: {total_time:.2f}s")
        
        if results["response_times"]:
            avg_response = sum(results["response_times"]) / len(results["response_times"])
            print(f"Average response time: {avg_response*1000:.2f}ms")
        
        if results["errors"]:
            print("\nTop errors:")
            for error, count in sorted(results["errors"].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"- {error}: {count} occurrences")

if __name__ == "__main__":
    try:
        run_load_test(
            total_trades=8000,
            batch_size=100,
            delay=0.1
        )
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")