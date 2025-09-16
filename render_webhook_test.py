#!/usr/bin/env python3
"""
Test Render webhook after deployment fix
"""

import requests
import json
import time
from datetime import datetime

def test_render_deployment():
    """Test if Render deployment is working after fixes"""
    
    print("🔍 Testing Render Deployment After Fix...")
    print(f"Time: {datetime.now()}")
    print("=" * 50)
    
    # Test 1: Basic connectivity
    try:
        print("📡 Testing basic connection...")
        response = requests.get('https://jarvis-quant-sys.onrender.com/', timeout=30)
        print(f"✅ Basic Connection: Status {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    # Test 2: Webhook endpoint
    test_signal = {
        'ticker': 'EUR_USD',
        'strategy.order.action': 'buy', 
        'close': 1.08500,
        'strategy': 'SevenSYS',
        'signal_strength': 45.0,
        'news_bias': 0.0,
        'trend_strength': 8.0,
        'stop_loss': 1.08200,
        'take_profit': 1.08900
    }
    
    print("\n🎯 Testing Webhook Endpoint...")
    print(f"Signal: {json.dumps(test_signal, indent=2)}")
    
    try:
        response = requests.post(
            'https://jarvis-quant-sys.onrender.com/webhook',
            json=test_signal,
            timeout=30
        )
        
        print(f"\n📊 WEBHOOK RESPONSE:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ WEBHOOK TEST PASSED!")
            return True
        else:
            print(f"❌ WEBHOOK FAILED - Status {response.status_code}")
            if "500" in str(response.status_code):
                print("   This indicates OANDA connection issues still exist")
                print("   Check Render environment variables and logs")
            return False
            
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return False

if __name__ == "__main__":
    success = test_render_deployment()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
