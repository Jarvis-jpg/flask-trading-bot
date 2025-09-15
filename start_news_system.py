#!/usr/bin/env python3
"""
NEWS SYSTEM STARTER - Simplified Launch
Starts the automated news system with better error handling
"""

import sys
import os
import traceback
import time
from datetime import datetime

def main():
    print("🤖 STARTING SEVENSYS NEWS SYSTEM")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print()
    
    try:
        print("🔍 Testing imports...")
        
        # Test basic imports
        import pandas as pd
        print("✅ pandas")
        
        import numpy as np
        print("✅ numpy")
        
        import requests
        print("✅ requests")
        
        import schedule
        print("✅ schedule")
        
        # Test custom imports
        try:
            import oanda_client
            print("✅ oanda_client")
        except ImportError as e:
            print(f"❌ oanda_client: {e}")
            
        try:
            import memory_logger
            print("✅ memory_logger")
        except ImportError as e:
            print(f"❌ memory_logger: {e}")
        
        print()
        print("🚀 Imports successful! Starting automated system...")
        print("-" * 50)
        
        # Import and start the main system
        from fully_automated_sevensys import FullyAutomatedSevenSYS
        
        # Initialize system
        print("🔧 Initializing SevenSYS...")
        trader = FullyAutomatedSevenSYS()
        
        # Configure trading
        instruments = ['EUR_USD', 'GBP_USD', 'USD_JPY']
        cycle_minutes = 30
        
        print(f"🎯 Trading instruments: {', '.join(instruments)}")
        print(f"📊 Analysis cycle: {cycle_minutes} minutes")
        print(f"📰 News updates: Every 15 minutes")
        print(f"🔑 NewsAPI key configured: {len(trader.newsapi_key)} chars")
        print()
        print("💡 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start the system
        trader.start_automated_trading(instruments, cycle_minutes)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n📋 Full traceback:")
        traceback.print_exc()
        print("\n💡 Check the error above for troubleshooting")
    
    print("\n👋 News system shutdown complete")

if __name__ == "__main__":
    main()
