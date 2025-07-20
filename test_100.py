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

def check_server():
    """Check if the trading server is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/")
        return True
    except:
        return False

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

def run_test(num_trades=100, delay=5):
    """Run Forex trading test"""
    if not check_server():
        print("❌ Error: Trading server is not running!")
        print("Please start the server first with 'python app.py'")
        return

    server_url = "http://127.0.0.1:5000"
    webhook_url = f"{server_url}/webhook"
    
    print("\n🤖 Jarvis Forex Trading Test")
    print(f"Testing {len(PAIRS)} currency pairs:")
    for pair in PAIRS:
        print(f"- {pair}")
    print(f"\nTotal trades: {num_trades}")
    print(f"Delay between trades: {delay}s")
    print(f"Estimated duration: {(num_trades * delay) / 60:.1f} minutes")
    
    input("\nPress Enter to start testing...")
    
    wins = 0
    losses = 0
    errors = 0
    
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
                        result = response.json()
                        trade_result = result.get('details', {}).get('result', 'unknown')
                        profit = result.get('details', {}).get('profit', 0)
                        
                        if trade_result == 'win':
                            wins += 1
                            status = '✅ WIN'
                        else:
                            losses += 1
                            status = '❌ LOSS'
                            
                        pbar.set_description(
                            f"{status} {trade['pair']} {trade['action']} (P/L: {profit:+.2f})"
                        )
                    else:
                        errors += 1
                        error_details = response.json()
                        error_msg = error_details.get('error', 'Unknown error')
                        print(f"\n❌ Server Error: {error_msg}")
                        if 'traceback' in error_details:
                            print("\nTraceback:")
                            print(error_details['traceback'])
                        pbar.set_description(f"❌ Error: {error_msg[:30]}...")
                        
                except Exception as e:
                    errors += 1
                    print(f"\n❌ Error: {str(e)}")
                
                pbar.update(1)
                
                # Show statistics every 10 trades
                if (i + 1) % 10 == 0:
                    total = wins + losses
                    win_rate = (wins / total * 100) if total > 0 else 0
                    print(f"\n📊 Statistics after {i + 1} trades:")
                    print(f"  Wins: {wins}")
                    print(f"  Losses: {losses}")
                    print(f"  Errors: {errors}")
                    print(f"  Win Rate: {win_rate:.1f}%")
                
                time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    
    # Print final statistics
    total = wins + losses
    win_rate = (wins / total * 100) if total > 0 else 0
    print("\n📊 Final Statistics:")
    print(f"  Total Trades: {total}")
    print(f"  Wins: {wins}")
    print(f"  Losses: {losses}")
    print(f"  Errors: {errors}")
    print(f"  Win Rate: {win_rate:.1f}%")

if __name__ == "__main__":
    # Run 100 test trades with 5 second delay
    run_test(num_trades=100, delay=5)
