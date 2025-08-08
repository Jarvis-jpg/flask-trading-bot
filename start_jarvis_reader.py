#!/usr/bin/env python3
"""
Start the Ultra-Reliable JARVIS Trading System
Quick launcher script
"""

import subprocess
import sys
import os

def start_jarvis_reader():
    """Start the ultra-reliable JARVIS system"""
    print("🚀 STARTING ULTRA-RELIABLE JARVIS TRADING SYSTEM")
    print("=" * 60)
    
    # Check if the jarvis_ultra_reliable.py file exists
    if not os.path.exists("jarvis_ultra_reliable.py"):
        print("❌ Error: jarvis_ultra_reliable.py not found in current directory")
        print("📁 Current directory:", os.getcwd())
        return False
    
    print("✅ Found jarvis_ultra_reliable.py")
    print("🤖 Starting automated Pine Script signal detection...")
    print("💰 5% risk per trade | Stop Loss: 20 pips | Take Profit: 40 pips")
    print("🎯 Will detect BUY/SELL signals from your Pine Script automatically")
    print("━" * 60)
    
    try:
        # Start the ultra-reliable system
        subprocess.run([sys.executable, "jarvis_ultra_reliable.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting JARVIS: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n⏹️  JARVIS system stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    start_jarvis_reader()
