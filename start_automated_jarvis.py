#!/usr/bin/env python3
"""
JARVIS Automated System Launcher
Simple launcher now that you've reset your TradingView password
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

def check_jarvis_status():
    """Check if JARVIS system is online"""
    try:
        response = requests.get("https://jarvis-quant-sys.onrender.com/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JARVIS System: ONLINE")
            print(f"   Balance: ${data.get('balance', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ JARVIS System: OFFLINE (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ JARVIS Connection Failed: {e}")
        return False

def launch_automated_reader():
    """Launch the automated Pine Script reader"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 🚀 LAUNCHING JARVIS AUTOMATED SYSTEM                        ║
║                     Password Reset - Ready to Go!                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT WILL HAPPEN:
✅ Chrome browser will open to TradingView
✅ You login with your RESET password (one time)
✅ System navigates to EUR/USD chart automatically
✅ Your Pine Script indicators will be read automatically
✅ BUY/SELL signals sent to JARVIS automatically
✅ JARVIS executes trades with 5% risk automatically

🔐 IMPORTANT: 
- Use your NEW reset password when TradingView opens
- After login, everything runs 100% automatically
- DO NOT close the browser window
- System will monitor and trade continuously

⏰ Starting in 3 seconds...
""")
    
    for i in range(3, 0, -1):
        print(f"⏳ {i}...")
        time.sleep(1)
    
    print("🚀 Launching automated reader...")
    
    try:
        # Launch the existing Pine Script reader
        subprocess.run([sys.executable, "jarvis_pine_script_reader.py"], check=False)
    except KeyboardInterrupt:
        print("\n👋 System stopped by user")
    except Exception as e:
        print(f"❌ Launch error: {e}")

def main():
    """Main launcher function"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🤖 JARVIS FULLY AUTOMATED LAUNCHER                       ║
║                          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Check JARVIS system first
    print("1️⃣  Checking JARVIS system status...")
    if not check_jarvis_status():
        print("❌ JARVIS system not available. Please check your internet connection.")
        return
    
    print("\n2️⃣  JARVIS system confirmed online!")
    
    # Launch automated reader
    print("\n3️⃣  Launching automated Pine Script reader...")
    launch_automated_reader()

if __name__ == "__main__":
    main()
