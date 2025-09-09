#!/usr/bin/env python3
"""
Test the restored webhook functionality
"""
import requests
import json
from datetime import datetime

def test_working_webhook():
    """Test the restored webhook with the exact format from your Render logs"""
    
    # This is the EXACT data format from your working Render logs
    test_data = {
        "ticker": "EURUSD",
        "strategy.order.action": "sell",
        "close": 1.17104,
        "strategy": "SevenSYS",
        "signal_strength": 58,
        "stop_loss": 1.1722152226,
        "take_profit": 1.1686895548
    }
    
    # Test locally first (if Flask running locally)
    local_url = "http://localhost:5000/webhook"
    render_url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    print("🧪 TESTING RESTORED WEBHOOK FUNCTIONALITY")
    print("="*50)
    print(f"Test Data: {json.dumps(test_data, indent=2)}")
    
    # Test local first
    try:
        print(f"\n📡 Testing LOCAL webhook: {local_url}")
        response = requests.post(local_url, json=test_data, timeout=10)
        print(f"✅ Local Status: {response.status_code}")
        print(f"📥 Local Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("⚠️  Local Flask not running (that's fine)")
    except Exception as e:
        print(f"❌ Local test error: {e}")
    
    # Test Render
    try:
        print(f"\n🌐 Testing RENDER webhook: {render_url}")
        response = requests.post(render_url, json=test_data, timeout=30)
        print(f"✅ Render Status: {response.status_code}")
        print(f"📥 Render Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ WEBHOOK RESTORED AND WORKING!")
        else:
            print("⚠️  Webhook responded but check the message")
            
    except requests.exceptions.Timeout:
        print("⏱️  Render timeout (might be cold start)")
    except Exception as e:
        print(f"❌ Render test error: {e}")

if __name__ == "__main__":
    test_working_webhook()
