#!/usr/bin/env python3
"""
JARVIS Autonomous Trading System Startup Script
Initializes and starts the complete autonomous trading system
"""

import os
import sys
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('startup.log'),
        logging.StreamHandler()
    ]
)

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    required_vars = [
        'OANDA_API_KEY',
        'OANDA_ACCOUNT_ID', 
        'OANDA_API_URL',
        'OANDA_LIVE'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    # Check if in live mode
    is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
    if is_live:
        print("⚠️  LIVE TRADING MODE DETECTED")
        print("💰 Real money will be used for trading!")
        
        # Add extra confirmation for live mode
        confirm = input("Type 'CONFIRM_LIVE_TRADING' to continue: ")
        if confirm != 'CONFIRM_LIVE_TRADING':
            print("❌ Live trading not confirmed. Exiting...")
            return False
    else:
        print("✅ PRACTICE MODE - Safe for testing")
    
    print("✅ Environment configuration valid")
    return True

def start_system():
    """Start the autonomous trading system"""
    print("🚀 Starting JARVIS Autonomous Trading System")
    print("=" * 50)
    
    try:
        # Import the live trading system
        from live_trading_system import live_trading_system
        
        # Start the system
        success = live_trading_system.start_trading()
        
        if success:
            print("✅ Autonomous trading system started successfully!")
            print("📊 System is now monitoring markets and executing trades...")
            print("🔄 Press Ctrl+C to stop the system")
            
            # Keep system running
            try:
                while live_trading_system.is_running:
                    time.sleep(1)
                    
                    # Print status every 5 minutes
                    if int(time.time()) % 300 == 0:
                        status = live_trading_system.get_status()
                        print(f"📈 Status: {status['daily_stats']['trades_count']} trades, "
                              f"${status['daily_stats']['profit_loss']:.2f} P&L")
                        
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
                live_trading_system.stop_trading()
                print("✅ System stopped safely")
                
        else:
            print("❌ Failed to start autonomous trading system")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import trading system: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🤖 JARVIS Autonomous Trading System")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check environment configuration
        if not check_environment():
            sys.exit(1)
        
        # Start the system
        if not start_system():
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
