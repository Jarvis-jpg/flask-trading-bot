#!/usr/bin/env python3
"""
Test the simplified market orders without TP/SL
"""
import requests
import json
import time

def test_simplified_orders():
    """Test the simplified market orders"""
    
    test_data = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "stop_loss": 1.1722152226,
        "take_profit": 1.1686895548
    }
    
    print("🧪 TESTING SIMPLIFIED MARKET ORDERS")
    print("="*50)
    print("Now placing market orders WITHOUT TP/SL to avoid conflicts")
    
    render_url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    # Give Render time to deploy
    print("⏱️  Waiting 30 seconds for Render to deploy...")
    time.sleep(30)
    
    try:
        print(f"📡 Testing: {render_url}")
        response = requests.post(render_url, json=test_data, timeout=30)
        print(f"✅ Status: {response.status_code}")
        
        result = response.json()
        print(f"📥 Result: {result['status']}")
        
        if result['status'] == 'success':
            print("🎉 SUCCESS! Market order placed successfully!")
            print("✅ Your TradingView alerts should now work!")
            if 'trade_data' in result:
                trade_data = result['trade_data']
                print(f"📊 Order ID: {trade_data.get('order_id', 'N/A')}")
                print(f"💰 Filled Price: {trade_data.get('filled_price', 'N/A')}")
        else:
            error_msg = result.get('message', 'No message')
            print(f"❌ Error: {error_msg[:100]}...")
            
            if 'precision' not in error_msg.lower() and 'loss' not in error_msg.lower():
                print("🎯 Different error - progress made!")
                
    except requests.exceptions.Timeout:
        print("⏱️  Timeout - try again, Render might still be deploying")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simplified_orders()
