#!/usr/bin/env python3
"""
JARVIS Pine Script Integration - Simple Launcher
Uses your existing Pine Script strategy - no custom coding needed
"""

import subprocess
import sys
import os

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 JARVIS PINE SCRIPT INTEGRATION                         ║  
║                     Uses Your Existing Strategy                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎉 GOOD NEWS: No custom strategies needed!
   
✅ This system reads the SAME indicators your Pine Script uses:
   • EMA 12 & 26 (exponential moving averages)
   • RSI 14 (relative strength index)  
   • MACD (moving average convergence divergence)
   • Bollinger Bands (volatility bands)
   • Trading session filters (London/NY)

✅ Uses the SAME trading logic as your Pine Script:
   • Buy when: Price > EMA12 > EMA26, RSI 30-70, MACD bullish
   • Sell when: Price < EMA12 < EMA26, RSI 30-70, MACD bearish
   • 70%+ confidence threshold (same as your Pine Script)
   • 5% risk per trade (same as your JARVIS system)

🚀 SETUP INSTRUCTIONS:

1️⃣ Open TradingView in your browser
2️⃣ Load ANY chart (EUR/USD recommended)  
3️⃣ Add these indicators to match your Pine Script:
   • EMA (12) - Exponential Moving Average
   • EMA (26) - Exponential Moving Average  
   • RSI (14) - Relative Strength Index
   • MACD (12, 26, 9) - MACD
   • Bollinger Bands (20, 2) - Bollinger Bands

4️⃣ Run this system - it will:
   ✅ Open TradingView automatically
   ✅ Read your indicators every 30 seconds
   ✅ Apply your Pine Script logic
   ✅ Send signals to JARVIS when conditions are met
   ✅ JARVIS executes trades through OANDA

💰 EXPECTED RESULTS:
   • Same signals as your Pine Script would generate
   • 70%+ confidence trades only  
   • 5% risk per trade
   • Works with TradingView FREE plan
   • 24/7 autonomous trading

🎯 READY TO START?
""")
    
    choice = input("Press ENTER to start JARVIS Pine Script Reader or 'q' to quit: ").strip().lower()
    
    if choice == 'q':
        print("👋 Goodbye!")
        return
    
    print("\n🚀 Starting JARVIS Pine Script Reader...")
    print("📊 This will open TradingView and start monitoring...")
    print("💡 Make sure your JARVIS system is running at: https://jarvis-quant-sys.onrender.com")
    print("🔄 System will start in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        # Run the Pine Script reader
        subprocess.run([sys.executable, "jarvis_pine_script_reader.py"])
    except KeyboardInterrupt:
        print("\n⏹️ JARVIS Pine Script Reader stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
