#!/usr/bin/env python3
"""
TradingView Free Setup Guide and Launcher
Complete setup instructions and easy launcher for the TradingView integration
"""

import os
import sys
import subprocess
import json
import requests
from datetime import datetime

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'selenium',
        'webdriver-manager', 
        'beautifulsoup4',
        'schedule',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ All dependencies installed!")
    
    return True

def verify_jarvis_connection():
    """Verify connection to JARVIS system"""
    print("\n🔗 Verifying JARVIS connection...")
    
    jarvis_url = "https://jarvis-quant-sys.onrender.com"
    
    try:
        response = requests.get(jarvis_url, timeout=10)
        if response.status_code == 200:
            print("✅ JARVIS system is online and accessible")
            return True
        else:
            print(f"⚠️ JARVIS returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to JARVIS: {e}")
        return False

def setup_guide():
    """Display complete setup guide"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📊 TRADINGVIEW FREE INTEGRATION SETUP                     ║
║                           Complete Setup Guide                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT THIS DOES:
   • Reads signals from TradingView FREE charts (no paid plan needed)
   • Automatically sends trading signals to your JARVIS system
   • Runs 24/7 autonomous trading without webhooks
   • Uses your custom trading strategy and indicators

📋 SETUP STEPS:

1️⃣ CUSTOMIZE YOUR CHART URL:
   • Go to TradingView.com
   • Set up your chart with indicators (EMA, MACD, RSI, etc.)
   • Copy your chart URL
   • Edit 'tradingview_config.py' and paste URL in CHART_URL

2️⃣ CUSTOMIZE YOUR STRATEGY:
   • Edit the 'custom_signal_logic()' function in tradingview_config.py
   • Add your trading rules (when to buy/sell)
   • Set confidence thresholds and risk parameters

3️⃣ RUN THE SYSTEM:
   • Execute: python tradingview_enhanced_reader.py
   • System will open TradingView, monitor your chart
   • Automatically send signals to JARVIS when conditions are met

🔧 CONFIGURATION FILES:
   • tradingview_config.py - Your trading strategy and settings
   • tradingview_enhanced_reader.py - Main monitoring system
   • tradingview_free_reader.py - Basic version (alternative)

⚙️ CUSTOMIZATION OPTIONS:
   • Chart monitoring interval (default: 30 seconds)  
   • Confidence threshold (default: 70%)
   • Risk per trade (default: 5%)
   • Currency pairs to monitor
   • Stop loss and take profit levels

🚀 ADVANCED FEATURES:
   • Multiple indicator support
   • Signal history tracking
   • Error handling and auto-restart
   • Duplicate signal prevention
   • Detailed logging

💡 STRATEGY EXAMPLES:
   • EMA crossover signals
   • RSI oversold/overbought
   • MACD histogram changes
   • Price momentum detection
   • Support/resistance breaks

🎯 NEXT STEPS:
   1. Run this setup: python setup_tradingview_free.py
   2. Edit tradingview_config.py with your strategy
   3. Test: python tradingview_enhanced_reader.py
   4. Monitor logs and profits!

════════════════════════════════════════════════════════════════════════════════
""")

def create_sample_strategy():
    """Create a sample trading strategy file"""
    print("\n📝 Creating sample strategy configuration...")
    
    sample_config = '''# Sample Trading Strategy Configuration

def custom_signal_logic(indicators, current_price, previous_signals):
    """
    SAMPLE STRATEGY: Simple EMA Crossover
    Replace this with your own trading logic
    """
    
    # Example: Generate buy signal on price momentum
    if len(previous_signals) > 0:
        last_price = previous_signals[-1].get('price', current_price)
        price_change_pct = ((current_price - last_price) / last_price) * 100
        
        # Strong bullish momentum - BUY signal
        if price_change_pct > 0.1:  # 0.1% price increase
            return {
                "action": "buy",
                "confidence": min(0.95, 0.75 + (price_change_pct / 100)),
                "reason": f"Bullish momentum: {price_change_pct:.2f}%"
            }
        
        # Strong bearish momentum - SELL signal  
        elif price_change_pct < -0.1:  # 0.1% price decrease
            return {
                "action": "sell",
                "confidence": min(0.95, 0.75 + (abs(price_change_pct) / 100)),
                "reason": f"Bearish momentum: {price_change_pct:.2f}%"
            }
    
    return None  # No signal

# Customize these settings:
CHART_URL = "https://www.tradingview.com/chart/"  # Your TradingView chart URL
CHECK_INTERVAL_SECONDS = 30  # How often to check for signals
CONFIDENCE_THRESHOLD = 0.75  # Minimum confidence to send signal
DEFAULT_RISK_PERCENTAGE = 5.0  # Risk per trade
'''
    
    with open("sample_strategy.py", "w") as f:
        f.write(sample_config)
    
    print("✅ Created sample_strategy.py - customize this with your trading logic!")

def launch_system():
    """Launch the TradingView monitoring system"""
    print("\n🚀 Launching TradingView Free Integration...")
    
    try:
        # Check if configuration exists
        if not os.path.exists("tradingview_config.py"):
            print("❌ Configuration file not found!")
            print("Please customize tradingview_config.py first")
            return False
        
        # Import and run the enhanced reader
        print("Starting enhanced TradingView reader...")
        subprocess.run([sys.executable, "tradingview_enhanced_reader.py"])
        
    except KeyboardInterrupt:
        print("\n⏹️ System stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error launching system: {e}")
        return False

def main():
    """Main setup and launcher function"""
    print("🔧 TradingView Free Integration Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Verify JARVIS connection
    if not verify_jarvis_connection():
        print("⚠️ Warning: Cannot connect to JARVIS - check your internet connection")
    
    # Show setup guide
    setup_guide()
    
    # Create sample strategy
    create_sample_strategy()
    
    # Ask user what to do
    print("\n🎯 WHAT WOULD YOU LIKE TO DO?")
    print("1. 📖 View setup guide (shown above)")
    print("2. 🔧 Edit configuration file") 
    print("3. 🚀 Launch TradingView monitoring")
    print("4. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            setup_guide()
        elif choice == "2":
            print(f"\n📝 Edit this file: {os.path.abspath('tradingview_config.py')}")
            print("Customize your trading strategy, chart URL, and settings")
        elif choice == "3":
            if launch_system():
                break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
