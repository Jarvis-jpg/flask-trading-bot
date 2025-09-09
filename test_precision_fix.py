#!/usr/bin/env python3
"""
Test with precision fix
"""
import requests
import json

def test_precision_fix():
    """Test the precision fix for TP/SL prices"""
    
    # Test data with high precision prices (the problematic ones)
    test_data = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "strategy": "SevenSYS",
        "signal_strength": 58,
        "stop_loss": 1.1722152226,      # 10 decimal places
        "take_profit": 1.1686895548     # 10 decimal places
    }
    
    print("🧪 TESTING PRECISION FIX")
    print("="*40)
    print(f"Original TP: {test_data['take_profit']}")
    print(f"Original SL: {test_data['stop_loss']}")
    print(f"Should round to 5 decimal places")
    print(f"Expected TP: {round(test_data['take_profit'], 5)}")
    print(f"Expected SL: {round(test_data['stop_loss'], 5)}")
    
    # Test local webhook
    try:
        print(f"\n📡 Testing LOCAL webhook...")
        response = requests.post("http://localhost:5000/webhook", json=test_data, timeout=10)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result['status']}")
        if 'trade_data' in result:
            print(f"✅ SUCCESS: Trade executed!")
        else:
            print(f"Message: {result.get('message', 'No message')[:100]}...")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Local Flask not running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_precision_fix()
