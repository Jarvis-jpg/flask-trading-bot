#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def test_webhook():
    url = "http://localhost:5000/webhook"
    
    # Test data simulating TradingView alert
    test_data = {
        "pair": "EURUSD",
        "action": "buy", 
        "entry": 1.0856,
        "stop_loss": 1.0806,
        "take_profit": 1.0956,
        "confidence": 0.85,
        "strategy": "JARVIS_TEST",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"Testing webhook: {url}")
    print(f"Sending: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check if memory was updated
        print("\nChecking memory update...")
        from live_trading_memory import live_memory
        live_memory.display_status()
        
    except requests.exceptions.ConnectionError:
        print("Connection failed - Flask is not running!")
        print("Start Flask first: python start_flask.py")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_webhook()
