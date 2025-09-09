#!/usr/bin/env python3
"""
Final test with all fixes applied
"""
import requests
import json
import time

def final_webhook_test():
    """Final test with all fixes applied"""
    
    test_data = {
        "ticker": "EURUSD",                 # Will be converted to EUR_USD
        "strategy.order.action": "sell",
        "close": 1.17104,
        "stop_loss": 1.1722152226,          # Will be rounded and ignored for now
        "take_profit": 1.1686895548         # Will be rounded and ignored for now
    }
    
    print("🎯 FINAL WEBHOOK TEST")
    print("="*50)
    print("✅ Fixed: Data format (ticker, strategy.order.action, close)")
    print("✅ Fixed: Symbol format (EURUSD -> EUR_USD)")  
    print("✅ Fixed: Price precision (rounded to 5 decimals)")
    print("✅ Fixed: Order type (market orders without TP/SL)")
    
    render_url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    # Wait for deployment
    print("\n⏱️  Waiting for Render deployment...")
    time.sleep(20)
    
    try:
        print(f"\n📡 Final test: {render_url}")
        response = requests.post(render_url, json=test_data, timeout=30)
        print(f"✅ Status: {response.status_code}")
        
        result = response.json()
        print(f"📥 Result: {result['status']}")
        
        if result['status'] == 'success':
            print("\n🎉🎉 SUCCESS! WEBHOOK IS WORKING! 🎉🎉")
            print("✅ Your TradingView alerts will now execute trades!")
            print("✅ Market orders will be placed on OANDA!")
            print("✅ Your trading system is LIVE and functional!")
            
            if 'trade_data' in result:
                trade_data = result['trade_data']
                print(f"\n📊 Trade Details:")
                print(f"   Order ID: {trade_data.get('order_id', 'N/A')}")
                print(f"   Filled Price: {trade_data.get('filled_price', 'N/A')}")
                print(f"   Timestamp: {trade_data.get('timestamp', 'N/A')}")
        else:
            error_msg = result.get('message', 'No message')
            print(f"\n❌ Still an error: {error_msg}")
            
            # Analyze the error
            if 'instrument' in error_msg.lower():
                print("🔧 Still an instrument format issue")
            elif 'precision' in error_msg.lower():
                print("🔧 Still a precision issue")  
            elif 'loss' in error_msg.lower():
                print("🔧 Still a TP/SL direction issue")
            else:
                print("🔧 New type of error - investigating...")
                
    except requests.exceptions.Timeout:
        print("⏱️  Timeout - try again")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    final_webhook_test()
