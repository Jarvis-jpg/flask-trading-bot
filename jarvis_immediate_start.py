#!/usr/bin/env python3
"""
JARVIS Immediate Start - No Dependencies
Works with existing browser session if needed
"""

import subprocess
import time
import requests
import webbrowser
from datetime import datetime

def check_jarvis():
    """Quick JARVIS check"""
    try:
        response = requests.get("https://jarvis-quant-sys.onrender.com/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JARVIS ONLINE - Balance: ${data.get('balance', 'Unknown')}")
            return True
        else:
            print(f"❌ JARVIS Status: {response.status_code}")
            return False
    except:
        print("❌ JARVIS Connection Failed")
        return False

def send_test_signal():
    """Send test signal to verify connection"""
    test_signal = {
        "action": "buy",
        "symbol": "EUR_USD",
        "confidence": 0.75,
        "risk_percentage": 5.0,
        "source": "immediate_test",
        "timestamp": datetime.now().isoformat(),
        "test_mode": True
    }
    
    try:
        response = requests.post("https://jarvis-quant-sys.onrender.com/webhook", 
                               json=test_signal, timeout=10)
        if response.status_code == 200:
            print("✅ Test signal successful - JARVIS receiving signals!")
            return True
        else:
            print(f"❌ Test signal failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test signal error: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🚀 JARVIS IMMEDIATE START                               ║
║                      Quick Setup & Verification                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    print("1️⃣  Checking JARVIS system...")
    if not check_jarvis():
        print("❌ Cannot connect to JARVIS. Check internet connection.")
        return
    
    print("\n2️⃣  Testing signal connection...")
    if not send_test_signal():
        print("❌ Signal connection failed.")
        return
    
    print("\n3️⃣  Opening TradingView...")
    webbrowser.open("https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD")
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ✅ SYSTEM VERIFIED & READY                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 NEXT STEPS (MANUAL FOR NOW):

1. 🔐 LOGIN to TradingView with your reset password
2. 📊 ADD your Pine Script to the EUR/USD chart  
3. 👀 WATCH for BUY/SELL signals from your Pine Script
4. 📱 MANUALLY send signals using this method:

   When you see a BUY signal:
   - Open terminal
   - Run: python -c "import requests; requests.post('https://jarvis-quant-sys.onrender.com/webhook', json={{'action':'buy','symbol':'EUR_USD','confidence':0.75,'risk_percentage':5.0}})"
   
   When you see a SELL signal:
   - Run: python -c "import requests; requests.post('https://jarvis-quant-sys.onrender.com/webhook', json={{'action':'sell','symbol':'EUR_USD','confidence':0.75,'risk_percentage':5.0}})"

🔥 ALTERNATIVE: Wait for the automated system to be fixed, or use this manual method to trade immediately!

📊 Monitor your trades: https://jarvis-quant-sys.onrender.com
💰 Risk per trade: 5% (automatic)
🎯 Stop Loss: 20 pips | Take Profit: 40 pips
""")

if __name__ == "__main__":
    main()
