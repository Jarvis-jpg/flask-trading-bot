#!/usr/bin/env python3
"""
Test the deployed Render version
"""
import requests
import json

def test_render_deployment():
    """Test the deployed webhook on Render"""
    
    # Use your original working data format
    test_data = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "strategy": "SevenSYS",
        "signal_strength": 58,
        "stop_loss": 1.1722152226,
        "take_profit": 1.1686895548
    }
    
    print("🌐 TESTING DEPLOYED RENDER WEBHOOK")
    print("="*50)
    print("Using your original working data format...")
    
    render_url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    try:
        print(f"📡 Sending to: {render_url}")
        response = requests.post(render_url, json=test_data, timeout=30)
        print(f"✅ Status: {response.status_code}")
        
        result = response.json()
        print(f"📥 Result: {result['status']}")
        
        if result['status'] == 'success':
            print("🎉 SUCCESS! Webhook is now working!")
            print("Your TradingView alerts should work correctly now.")
        else:
            error_msg = result.get('message', 'No message')
            print(f"❌ Error: {error_msg[:200]}...")
            
            if 'precision' in error_msg.lower():
                print("🔧 Still a precision issue - but we fixed that!")
            elif 'direction' in error_msg.lower() or 'loss' in error_msg.lower():
                print("🔧 Still a direction issue - investigating...")
                
    except requests.exceptions.Timeout:
        print("⏱️  Timeout - Render might be cold starting, try again")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_render_deployment()
