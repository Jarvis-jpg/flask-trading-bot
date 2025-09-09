#!/usr/bin/env python3
"""
Debug the TP/SL direction issue by checking current market prices
"""
import requests
import json

def test_with_market_price():
    """Test by getting current market price first"""
    
    print("🔍 DEBUGGING TP/SL DIRECTION ISSUES")
    print("="*50)
    
    # Let's test with the EXACT format that was working in your Render logs
    # From your logs: this was SUCCESSFUL
    working_data = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "stop_loss": 1.1722152226,    # This WAS working before
        "take_profit": 1.1686895548   # This WAS working before
    }
    
    print("📊 Testing with YOUR ORIGINAL WORKING DATA:")
    print(f"  Action: {working_data['strategy.order.action']}")
    print(f"  Entry (close): {working_data['close']}")
    print(f"  Stop Loss: {working_data['stop_loss']}")
    print(f"  Take Profit: {working_data['take_profit']}")
    
    # For SELL:
    # - Entry: 1.17104
    # - SL: 1.17222 (ABOVE entry) ✅ Correct for SELL
    # - TP: 1.16869 (BELOW entry) ✅ Correct for SELL
    
    print(f"\n📈 Direction Analysis for SELL:")
    entry = working_data['close']
    sl = working_data['stop_loss'] 
    tp = working_data['take_profit']
    
    print(f"  Entry: {entry}")
    print(f"  SL: {sl} ({'ABOVE' if sl > entry else 'BELOW'} entry) {'✅' if sl > entry else '❌'}")
    print(f"  TP: {tp} ({'ABOVE' if tp > entry else 'BELOW'} entry) {'✅' if tp < entry else '❌'}")
    
    # Test the webhook
    try:
        print(f"\n📡 Testing webhook...")
        response = requests.post("http://localhost:5000/webhook", json=working_data, timeout=10)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Result: {result['status']}")
        
        if result['status'] == 'success':
            print(f"✅ SUCCESS! Trade executed!")
        else:
            error_msg = result.get('message', 'No message')
            print(f"❌ Error: {error_msg[:100]}...")
            
            # Try to decode the OANDA error
            if 'orderRejectTransaction' in error_msg:
                try:
                    error_data = json.loads(error_msg)
                    reject_reason = error_data.get('orderRejectTransaction', {}).get('rejectReason', 'Unknown')
                    print(f"🔍 OANDA Reject Reason: {reject_reason}")
                except:
                    pass
                    
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_with_market_price()
