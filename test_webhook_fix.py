#!/usr/bin/env python3
"""
Quick webhook test to verify the fix is deployed
"""

import requests
import time
import json

def test_webhook_fix():
    """Test if the webhook fix is live"""
    print("🔍 TESTING WEBHOOK FIX DEPLOYMENT")
    print("=" * 50)
    
    # Test data with 'symbol' instead of 'pair' (this should work after fix)
    test_signal = {
        "action": "buy",
        "symbol": "EURUSD",  # Using 'symbol' instead of 'pair'
        "price": 1.0850,
        "confidence": 0.75,
        "risk_reward_ratio": 2.0,
        "timeframe": "15m"
    }
    
    webhook_url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    print(f"📡 Testing webhook with 'symbol' field...")
    print(f"   URL: {webhook_url}")
    print(f"   Data: {json.dumps(test_signal, indent=2)}")
    
    try:
        response = requests.post(
            webhook_url,
            json=test_signal,
            timeout=15
        )
        
        print(f"\n📊 RESULT:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS - Webhook fix is LIVE!")
            print("   🎯 Your trading signals will now process correctly!")
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}")
        elif response.status_code == 500:
            print("   ❌ STILL BROKEN - KeyError 'pair' likely still present")
            print("   ⏳ Render may still be deploying the fix...")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
        return response.status_code
        
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return None

def monitor_deployment():
    """Monitor until the fix is deployed"""
    print("\n🔄 MONITORING DEPLOYMENT...")
    print("Will check every 30 seconds until fix is live")
    
    attempts = 0
    max_attempts = 10  # 5 minutes max
    
    while attempts < max_attempts:
        attempts += 1
        print(f"\n📊 Attempt {attempts}/{max_attempts}:")
        
        status = test_webhook_fix()
        
        if status == 200:
            print("\n🎉 WEBHOOK FIX IS LIVE!")
            print("🚀 Your trading system should now work perfectly!")
            break
        elif status == 500:
            print("\n⏳ Still deploying... waiting 30 seconds")
            time.sleep(30)
        else:
            print("\n⚠️  Unexpected response, waiting 30 seconds")
            time.sleep(30)
    
    if attempts >= max_attempts:
        print("\n⏰ Monitoring timeout - check manually or wait longer")

if __name__ == "__main__":
    test_webhook_fix()
    
    # Ask if user wants to monitor
    monitor = input("\n🔄 Monitor deployment progress? (y/n): ").lower().strip()
    if monitor == 'y':
        monitor_deployment()
