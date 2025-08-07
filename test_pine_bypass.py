#!/usr/bin/env python3
"""
Test Pine Script bypass mode with exact JARVIS signal format
"""

import requests
import json

# Test data that matches exactly what JARVIS ultra-reliable system sends
jarvis_signal = {
    "symbol": "EURUSD",
    "action": "BUY", 
    "confidence": 85.0,  # This triggers Pine Script bypass mode
    "price": 1.0850,
    "timestamp": "2024-08-06T16:00:00Z",
    "risk": 5.0,
    "stop_loss": 20,
    "take_profit": 40
}

print("🚀 TESTING PINE SCRIPT BYPASS MODE")
print("=" * 50)
print(f"Signal data (exactly like JARVIS sends):")
print(json.dumps(jarvis_signal, indent=2))

url = "https://jarvis-quant-sys.onrender.com/webhook"

try:
    response = requests.post(url, json=jarvis_signal, timeout=30)
    print(f"\n✅ Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if "executed" in response.text.lower():
        print("\n🎉 SUCCESS! Trade should be executed!")
    elif "rejected" in response.text.lower():
        print("\n❌ Still rejected - checking reason...")
        if "market_data_unavailable" in response.text:
            print("   Issue: Market data still unavailable")
        elif "unfavorable_analysis" in response.text:
            print("   Issue: Analysis still failing")
    else:
        print(f"\n📊 Unexpected response - checking...")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print(f"\n🔧 PINE SCRIPT BYPASS LOGIC:")
print(f"✅ Signal has 'confidence': {jarvis_signal.get('confidence', 0) > 0}")
print(f"✅ Signal has valid 'action': {jarvis_signal.get('action') in ['BUY', 'SELL']}")
print(f"✅ Should bypass market analysis and execute directly!")
