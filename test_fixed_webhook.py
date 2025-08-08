#!/usr/bin/env python3
"""
Test Fixed Webhook with Valid FOREX Data
"""
import requests
import json

def test_fixed_webhook():
    """Test the fixed webhook with valid FOREX data"""
    
    print("🧪 TESTING FIXED WEBHOOK SYSTEM")
    print("="*50)
    
    webhook_url = "http://localhost:5000/webhook"
    
    # Test with valid FOREX pair (what TradingView should send)
    valid_trade = {
        "pair": "EURUSD",
        "action": "buy",
        "entry": 1.0856,
        "stop_loss": 1.0806,
        "take_profit": 1.0956,
        "confidence": 0.75,
        "strategy": "JARVIS_MultiSignal",
        "risk_reward": 2.0,
        "position_size": 10000,
        "timestamp": "1642780800"
    }
    
    print("📊 Testing Valid FOREX Trade:")
    print(json.dumps(valid_trade, indent=2))
    
    try:
        response = requests.post(webhook_url, json=valid_trade, timeout=10)
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📝 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'executed':
                print("🎉 SUCCESS: Trade would be executed!")
            elif result.get('status') == 'rejected':
                print(f"⚠️  REJECTED: {result.get('reason')}")
            else:
                print(f"📋 STATUS: {result.get('status')}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Flask server not running")
        print("   Start with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test with invalid crypto pair (should be rejected)
    print(f"\n" + "="*50)
    print("📊 Testing Invalid Crypto Trade (should be rejected):")
    
    crypto_trade = {
        "pair": "ETHUSDT",
        "action": "buy", 
        "entry": 2288.73,
        "stop_loss": 2246.55,
        "take_profit": 2357.76,
        "confidence": 0.91,
        "strategy": "CRYPTO_Test"
    }
    
    print(json.dumps(crypto_trade, indent=2))
    
    try:
        response = requests.post(webhook_url, json=crypto_trade, timeout=10)
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📝 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.json().get('status') == 'rejected':
            print("✅ CORRECT: Crypto pair properly rejected!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Flask server not running")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n" + "="*50)
    print("📋 SUMMARY:")
    print("1. ✅ FOREX pairs (EURUSD, GBPUSD, etc.) should be ACCEPTED")
    print("2. ❌ Crypto pairs (ETHUSDT, BTCUSDT, etc.) should be REJECTED")
    print("3. 🔧 Stop loss validation should work correctly")
    print("4. 📡 Make sure TradingView chart is on FOREX pair, not crypto")

if __name__ == "__main__":
    test_fixed_webhook()
