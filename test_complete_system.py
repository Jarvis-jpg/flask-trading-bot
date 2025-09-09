import requests
import json
from datetime import datetime

def test_sevensys_webhook():
    """Test the complete SevenSYS webhook system with TP/SL"""
    
    # Realistic SevenSYS alert data matching the Pine script format
    sevensys_alert = {
        "ticker": "EURUSD",
        "strategy.order.action": "buy",
        "close": "1.05234",
        "stop_loss": "1.04897",  # ~33.7 pips distance
        "take_profit": "1.06008"  # ~77.4 pips distance
    }
    
    print(f"Testing SevenSYS webhook with data:")
    print(json.dumps(sevensys_alert, indent=2))
    print(f"\nSL Distance: {(float(sevensys_alert['close']) - float(sevensys_alert['stop_loss'])) * 10000:.1f} pips")
    print(f"TP Distance: {(float(sevensys_alert['take_profit']) - float(sevensys_alert['close'])) * 10000:.1f} pips")
    print(f"Risk/Reward: {((float(sevensys_alert['take_profit']) - float(sevensys_alert['close'])) / (float(sevensys_alert['close']) - float(sevensys_alert['stop_loss']))):.2f}")
    
    try:
        # Test locally if running
        try:
            response = requests.post(
                'http://localhost:5000/webhook', 
                json=sevensys_alert,
                timeout=10
            )
            print(f"\nLocal webhook response: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.exceptions.ConnectionError:
            print("\nLocal server not running, testing production...")
            
            # Test production webhook
            response = requests.post(
                'https://jarvis-quant-sys.onrender.com/webhook', 
                json=sevensys_alert,
                timeout=30
            )
            print(f"\nProduction webhook response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error testing webhook: {e}")

def test_sell_signal():
    """Test a SELL signal from SevenSYS"""
    
    sevensys_sell_alert = {
        "ticker": "GBPUSD",
        "strategy.order.action": "sell",
        "close": "1.24567",
        "stop_loss": "1.24890",  # ~32.3 pips distance
        "take_profit": "1.23890"  # ~67.7 pips distance
    }
    
    print(f"\nTesting SELL signal:")
    print(json.dumps(sevensys_sell_alert, indent=2))
    print(f"SL Distance: {(float(sevensys_sell_alert['stop_loss']) - float(sevensys_sell_alert['close'])) * 10000:.1f} pips")
    print(f"TP Distance: {(float(sevensys_sell_alert['close']) - float(sevensys_sell_alert['take_profit'])) * 10000:.1f} pips")
    
    try:
        response = requests.post(
            'https://jarvis-quant-sys.onrender.com/webhook', 
            json=sevensys_sell_alert,
            timeout=30
        )
        print(f"SELL signal response: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error testing SELL signal: {e}")

if __name__ == "__main__":
    print("=== Testing Complete SevenSYS System ===")
    print(f"Test time: {datetime.now()}")
    
    test_sevensys_webhook()
    test_sell_signal()
    
    print("\n=== Test Complete ===")
    print("Check OANDA account and logs for trade execution details.")
    print("TP/SL should be added after market order fills.")
