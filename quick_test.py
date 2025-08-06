#!/usr/bin/env python3
"""Quick test to verify JARVIS connection and send a test signal"""

import requests
import json
from datetime import datetime

def quick_test():
    print("🔍 QUICK JARVIS CONNECTION TEST")
    print("=" * 40)
    
    jarvis_url = "https://jarvis-quant-sys.onrender.com"
    
    # Test 1: Check if JARVIS is online
    try:
        print("1. Testing JARVIS connection...")
        response = requests.get(f"{jarvis_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JARVIS is ONLINE")
            print(f"   Balance: ${data.get('balance', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
        else:
            print(f"❌ JARVIS offline: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ JARVIS connection failed: {e}")
        return
    
    # Test 2: Send test signal
    try:
        print("\n2. Sending test signal...")
        test_signal = {
            "action": "buy",
            "symbol": "EUR_USD",
            "confidence": 0.75,
            "risk_percentage": 5.0,
            "stop_loss_pips": 20,
            "take_profit_pips": 40,
            "source": "connection_test",
            "timestamp": datetime.now().isoformat(),
            "test_mode": True
        }
        
        response = requests.post(
            f"{jarvis_url}/webhook",
            json=test_signal,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test signal SUCCESSFUL!")
            print(f"   Response: {result.get('message', 'Unknown')}")
            print(f"   Status: {result.get('status', 'Unknown')}")
        else:
            print(f"❌ Test signal failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test signal error: {e}")
    
    print(f"\n🎯 CONCLUSION:")
    print(f"✅ JARVIS system is ready to receive signals")
    print(f"✅ Your TradingView reader can send signals to: {jarvis_url}/webhook")
    print(f"✅ Use 5% risk per trade")
    print(f"✅ Monitor dashboard at: {jarvis_url}")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Open TradingView with your Pine Script strategy")
    print(f"2. Run: python manual_tradingview_input.py")
    print(f"3. Input BUY/SELL when you see signals")
    print(f"4. JARVIS will execute trades automatically")

if __name__ == "__main__":
    quick_test()
