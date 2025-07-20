import requests
import json
from datetime import datetime, UTC, timedelta
import random
import time
from tqdm import tqdm

# Forex pairs configuration
PAIRS = {
    "EURUSD": {"base": 1.0950, "volatility": 0.0020, "pip": 0.0001},
    "GBPUSD": {"base": 1.2750, "volatility": 0.0025, "pip": 0.0001},
    "USDJPY": {"base": 143.50, "volatility": 0.1500, "pip": 0.01},
    "AUDUSD": {"base": 0.6750, "volatility": 0.0015, "pip": 0.0001},
    "USDCAD": {"base": 1.3450, "volatility": 0.0020, "pip": 0.0001},
    "NZDUSD": {"base": 0.6250, "volatility": 0.0015, "pip": 0.0001},
    "EURGBP": {"base": 0.8550, "volatility": 0.0015, "pip": 0.0001},
    "EURJPY": {"base": 157.50, "volatility": 0.2000, "pip": 0.01}
}

def generate_trade():
    """Generate realistic Forex trade data"""
    pair = random.choice(list(PAIRS.keys()))
    pair_info = PAIRS[pair]
    
    # Generate realistic price movement
    price = round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 4)
    
    # Calculate pips for SL and TP (10-30 pips for SL, 20-60 pips for TP)
    sl_pips = random.uniform(10, 30) * pair_info["pip"]
    tp_pips = random.uniform(20, 60) * pair_info["pip"]
    
    action = random.choice(["buy", "sell"])
    
    if action == "buy":
        stop_loss = round(price - sl_pips, 4)
        take_profit = round(price + tp_pips, 4)
    else:
        stop_loss = round(price + sl_pips, 4)
        take_profit = round(price - tp_pips, 4)
    
    return {
        "pair": pair,
        "action": action,
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": round(random.uniform(0.65, 0.95), 2),
        "strategy": "MA_Cross",
        "timestamp": datetime.now(UTC).isoformat().replace('+00:00', 'Z')
    }

def run_test(num_trades=8000, delay=5):
    """Run Forex trading test"""
    server_url = "http://127.0.0.1:5000"
    webhook_url = f"{server_url}/webhook"
    
    print("\n🤖 Jarvis Forex Trading Test")
    print(f"Testing {len(PAIRS)} currency pairs:")
    for pair in PAIRS:
        print(f"- {pair}")
    print(f"\nTotal trades: {num_trades}")
    print(f"Delay between trades: {delay}s")
    print(f"Estimated duration: {(num_trades * delay) / 3600:.1f} hours")
    
    input("\nPress Enter to start testing...")
    
    try:
        with tqdm(total=num_trades, desc="Processing trades") as pbar:
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
                        pbar.set_description(f"✅ {trade['pair']} {trade['action']}")
                    else:
                        pbar.set_description(f"❌ Error: {response.status_code}")
                        
                except Exception as e:
                    print(f"\n❌ Error: {str(e)}")
                
                pbar.update(1)
                time.sleep(delay)
                
                # Show periodic statistics
                if (i + 1) % 100 == 0:
                    print(f"\nCompleted {i + 1} trades")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")

if __name__ == "__main__":
    run_test()