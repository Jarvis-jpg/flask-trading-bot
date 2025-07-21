#!/usr/bin/env python3
"""
Jarvis Trading Bot Startup Script
This script initializes and starts the complete trading system
"""
import os
import sys
import time
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'models', 'trades', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ Directory created/verified: {directory}")

def test_system_components():
    """Test all system components"""
    logger.info("🔍 Testing system components...")
    
    try:
        # Test imports
        from dotenv import load_dotenv
        load_dotenv()
        
        from oanda_client import OandaClient
        from enhanced_trading_strategy import trading_strategy
        from autonomous_trading_engine import autonomous_engine
        from trade_analyzer import TradeAnalyzer
        
        logger.info("✅ All imports successful")
        
        # Test OANDA connection
        try:
            oanda = OandaClient()
            price_data = oanda.get_current_price('EUR_USD')
            logger.info(f"✅ OANDA connection: EUR_USD = {price_data.get('bid', 'N/A')}/{price_data.get('ask', 'N/A')}")
        except Exception as e:
            logger.error(f"❌ OANDA connection failed: {e}")
            return False
        
        # Test strategy
        try:
            import pandas as pd
            import numpy as np
            
            # Create sample data
            dates = pd.date_range(end=datetime.now(), periods=100, freq='1H')
            prices = np.random.normal(1.0950, 0.01, 100).cumsum() * 0.001 + 1.0950
            
            sample_data = pd.DataFrame({
                'datetime': dates,
                'open': prices * 0.9999,
                'high': prices * 1.0002,
                'low': prices * 0.9998,
                'close': prices,
                'volume': np.random.randint(1000, 5000, 100)
            }).set_index('datetime')
            
            signal = trading_strategy.generate_trade_signal('EUR_USD', sample_data)
            logger.info(f"✅ Strategy test: Signal = {signal['signal']}, Confidence = {signal['confidence']:.2f}")
        except Exception as e:
            logger.error(f"❌ Strategy test failed: {e}")
            return False
        
        logger.info("✅ All system components tested successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ System component test failed: {e}")
        return False

def start_flask_server():
    """Start the Flask web server"""
    logger.info("🚀 Starting Flask server...")
    
    try:
        from app import app
        
        # Start server in debug mode for development
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Set to False for production
            use_reloader=False  # Prevent double startup in debug mode
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start Flask server: {e}")
        return False

def main():
    """Main startup function"""
    print("🤖 Jarvis Autonomous Trading Bot")
    print("=" * 50)
    print(f"🕐 Startup Time: {datetime.now()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 50)
    
    # Create necessary directories
    create_directories()
    
    # Test system components
    if not test_system_components():
        logger.error("❌ System tests failed. Cannot start trading bot.")
        sys.exit(1)
    
    # Additional system info
    logger.info("📊 System Configuration:")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    mode = "LIVE" if os.getenv('OANDA_LIVE', 'false').lower() == 'true' else "PRACTICE"
    logger.info(f"   Trading Mode: {mode}")
    logger.info(f"   Account ID: {os.getenv('OANDA_ACCOUNT_ID', 'Not set')}")
    logger.info(f"   API URL: {os.getenv('OANDA_API_URL', 'Not set')}")
    
    # Final checks
    logger.info("✅ System ready for trading!")
    logger.info("🌐 Starting web interface...")
    logger.info("   Dashboard: http://localhost:5000")
    logger.info("   Test Connection: http://localhost:5000/test_connection")
    logger.info("   Webhook: http://localhost:5000/webhook")
    
    # Start Flask server
    start_flask_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
