#!/usr/bin/env python3
"""
Test production webhook fix
"""

import requests
import json

# Test data with 'symbol' field (TradingView format)
test_data = {
    "symbol": "EURUSD",
    "action": "BUY", 
    "price": 1.0850,
    "timestamp": "2024-01-01T12:00:00Z"
}

print("🚀 Testing production webhook fix...")
print(f"Test data: {json.dumps(test_data, indent=2)}")

url = "https://jarvis-quant-sys.onrender.com/webhook"

try:
    response = requests.post(url, json=test_data, timeout=30)
    print(f"\n✅ Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if "pair" in response.text and "KeyError" not in response.text:
        print("\n🎉 SUCCESS! Webhook fix is working!")
    elif "KeyError" in response.text:
        print("\n❌ Still getting KeyError - fix not deployed yet")
    else:
        print(f"\n📊 Response received - analyzing...")
        
except Exception as e:
    print(f"\n❌ Error testing webhook: {e}")
