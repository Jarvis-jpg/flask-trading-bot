"""
OANDA Environment Test - Try both practice and live environments
"""

import oandapyV20
import oandapyV20.endpoints.instruments as instruments

# Your credentials
api_key = "e9e9a0366a2b21ebbb03b965301f0182-ea0448d5fc88dd622b361855758d7f3e"
account_id = "001-001-12623605-001"

print("🔧 Testing OANDA API with different environments...")

# Test 1: Practice Environment
print("\n1️⃣ Testing PRACTICE environment...")
try:
    api_practice = oandapyV20.API(access_token=api_key, environment="practice")
    
    params = {"count": 5, "granularity": "M1", "price": "M"}
    request = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    response = api_practice.request(request)
    
    print("✅ PRACTICE environment works!")
    print(f"✅ Got {len(response['candles'])} candles")
    
except Exception as e:
    print(f"❌ PRACTICE failed: {e}")

# Test 2: Live Environment  
print("\n2️⃣ Testing LIVE environment...")
try:
    api_live = oandapyV20.API(access_token=api_key, environment="live")
    
    params = {"count": 5, "granularity": "M1", "price": "M"}
    request = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    response = api_live.request(request)
    
    print("✅ LIVE environment works!")
    print(f"✅ Got {len(response['candles'])} candles")
    
    # If live works, show sample data
    if response['candles']:
        latest = response['candles'][-1]
        print(f"✅ Latest EUR/USD: {latest['mid']['c']}")
        print(f"✅ Time: {latest['time']}")
    
except Exception as e:
    print(f"❌ LIVE failed: {e}")

print("\n🎯 CONCLUSION:")
print("- If PRACTICE works: Use 'practice' environment")
print("- If LIVE works: Use 'live' environment") 
print("- If both fail: Need new API credentials")
print("\n📝 This has NOTHING to do with git/deployment!")
print("🏠 Everything runs locally on your computer")
