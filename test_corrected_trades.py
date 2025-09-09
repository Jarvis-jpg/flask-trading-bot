#!/usr/bin/env python3
"""
Test with corrected stop loss direction
"""
import requests
import json

def test_corrected_trade():
    """Test with properly corrected stop loss direction"""
    
    # BUY trade with CORRECTED stop loss (below entry price)
    buy_test = {
        "ticker": "EURUSD",
        "strategy.order.action": "buy",
        "close": 1.17104,
        "stop_loss": 1.16900,      # BELOW entry (correct for BUY)
        "take_profit": 1.17400     # ABOVE entry (correct for BUY)
    }
    
    # SELL trade with CORRECTED stop loss (above entry price) 
    sell_test = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "stop_loss": 1.17300,     # ABOVE entry (correct for SELL)
        "take_profit": 1.16800    # BELOW entry (correct for SELL)
    }
    
    print("🧪 TESTING CORRECTED STOP LOSS DIRECTIONS")
    print("="*50)
    
    tests = [
        ("BUY Test", buy_test),
        ("SELL Test", sell_test)
    ]
    
    for test_name, test_data in tests:
        print(f"\n📊 {test_name}:")
        print(f"  Entry: {test_data['close']}")
        print(f"  Stop Loss: {test_data['stop_loss']}")
        print(f"  Take Profit: {test_data['take_profit']}")
        
        try:
            response = requests.post("http://localhost:5000/webhook", json=test_data, timeout=10)
            print(f"  Status: {response.status_code}")
            result = response.json()
            print(f"  Result: {result['status']}")
            
            if result['status'] == 'success':
                print(f"  ✅ SUCCESS!")
            else:
                print(f"  ❌ Error: {result.get('message', 'Unknown error')[:60]}...")
                
        except Exception as e:
            print(f"  ❌ Test failed: {e}")

if __name__ == "__main__":
    test_corrected_trade()
