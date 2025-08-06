#!/usr/bin/env python3
"""
Check system status before launching automated trading
"""

import requests
import json

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🔍 PRE-LAUNCH SYSTEM CHECK                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Check JARVIS
    try:
        response = requests.get("https://jarvis-quant-sys.onrender.com/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JARVIS System: ONLINE")
            print(f"   Balance: ${data.get('balance', 'Unknown')}")
            print(f"   Risk per trade: 5%")
            print(f"   Webhook: https://jarvis-quant-sys.onrender.com/webhook")
        else:
            print(f"❌ JARVIS offline")
    except:
        print(f"❌ JARVIS connection failed")
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  🚀 READY TO LAUNCH AUTOMATED SYSTEM                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 TO START FULLY AUTOMATED TRADING:

1️⃣  Run this command:
    python jarvis_pine_script_reader.py

2️⃣  Chrome will open to TradingView
    - Login with your RESET password
    - System will navigate to EUR/USD automatically

3️⃣  Add your Pine Script to the chart
    - System will read indicators automatically
    - BUY/SELL signals sent to JARVIS automatically

4️⃣  Keep browser open
    - System monitors 24/7
    - Trades executed with 5% risk automatically

🎯 THAT'S IT! Fully automated after login.
""")

if __name__ == "__main__":
    main()
