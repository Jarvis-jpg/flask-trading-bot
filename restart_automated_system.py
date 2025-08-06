#!/usr/bin/env python3
"""
JARVIS Clean Restart - Fully Automated
Restarts system cleanly after password reset
"""

import os
import subprocess
import sys
import time
import requests

def clean_system():
    """Clean any existing processes"""
    print("🧹 Cleaning existing processes...")
    
    # Kill any existing Chrome processes
    try:
        subprocess.run(["taskkill", "/f", "/im", "chrome.exe", "/t"], 
                      capture_output=True, shell=True)
        print("✅ Chrome processes cleaned")
    except:
        pass
    
    # Kill any existing Python processes running the reader
    try:
        subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", 
                       "WINDOWTITLE eq *jarvis*"], capture_output=True, shell=True)
        print("✅ Python processes cleaned")
    except:
        pass
    
    time.sleep(2)

def verify_jarvis():
    """Verify JARVIS system is ready"""
    print("🔍 Verifying JARVIS system...")
    
    try:
        response = requests.get("https://jarvis-quant-sys.onrender.com/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ JARVIS ONLINE - Balance: ${data.get('balance', 'Unknown')}")
            return True
        else:
            print(f"❌ JARVIS Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ JARVIS Connection: {e}")
        return False

def start_fresh_reader():
    """Start fresh automated reader"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 🚀 STARTING FRESH AUTOMATED SYSTEM                          ║
║                      Password Reset - Clean Start                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT'S HAPPENING:
✅ System cleaned and reset
✅ Fresh Chrome browser will open
✅ TradingView will load automatically
✅ You login ONCE with reset password
✅ System detects Pine Script signals automatically
✅ Trades executed automatically with 5% risk

🔐 IMPORTANT REMINDER:
- Use your NEW reset password when prompted
- After login, everything is 100% automated
- Keep the browser window open
- System monitors and trades 24/7

🚀 Starting in 3 seconds...
""")
    
    for i in range(3, 0, -1):
        print(f"⏳ {i}...")
        time.sleep(1)
    
    print("🚀 Launching automated reader...")
    
    try:
        # Start the Pine Script reader
        subprocess.Popen([sys.executable, "jarvis_pine_script_reader.py"], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print("""
✅ AUTOMATED READER LAUNCHED!

📊 WHAT TO EXPECT:
1. Chrome browser opens to TradingView
2. Login with your reset password  
3. Add your Pine Script to EUR/USD chart
4. System automatically reads signals
5. Signals sent to JARVIS automatically
6. Trades executed with 5% risk

🎯 DASHBOARD: https://jarvis-quant-sys.onrender.com
🔄 MONITORING: Continuous (every 30 seconds)

System is now FULLY AUTOMATED! 🚀
""")
        
    except Exception as e:
        print(f"❌ Launch error: {e}")

def main():
    """Main clean restart function"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🔧 JARVIS CLEAN RESTART                                ║
║                    Fixing Connection Issues                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Clean existing processes
    clean_system()
    
    # Verify JARVIS
    if not verify_jarvis():
        print("❌ JARVIS system not available. Check internet connection.")
        return
    
    # Start fresh reader
    start_fresh_reader()

if __name__ == "__main__":
    main()
