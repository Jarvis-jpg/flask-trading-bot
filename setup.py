#!/usr/bin/env python3
"""
Quick Setup and Installation Script for Jarvis Trading Bot
"""
import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    logger.info(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install all required packages"""
    logger.info("📦 Installing required packages...")
    
    requirements = [
        "flask",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "ta>=0.10.0",
        "python-dotenv>=0.19.0",
        "oandapyV20>=0.7.0",
        "requests>=2.25.0",
        "joblib>=1.0.0"
    ]
    
    for package in requirements:
        try:
            logger.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install {package}: {e}")
            return False
    
    logger.info("✅ All packages installed successfully")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "models", 
        "trades",
        "data",
        "strategies",
        "utils"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ Created directory: {directory}")

def check_environment_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        logger.warning("⚠️ .env file not found. Please ensure it contains:")
        logger.warning("   - OANDA_API_KEY")
        logger.warning("   - OANDA_ACCOUNT_ID")
        logger.warning("   - OANDA_API_URL")
        return False
    
    # Check if required variables are present
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = ['OANDA_API_KEY', 'OANDA_ACCOUNT_ID', 'OANDA_API_URL']
    missing_vars = [var for var in required_vars if var not in content]
    
    if missing_vars:
        logger.warning(f"⚠️ Missing environment variables in .env: {missing_vars}")
        return False
    
    logger.info("✅ Environment file configured")
    return True

def run_quick_test():
    """Run a quick system test"""
    logger.info("🔍 Running quick system test...")
    
    try:
        # Test imports
        import flask
        import pandas as pd
        import numpy as np
        import sklearn
        import ta
        import oandapyV20
        logger.info("✅ All imports successful")
        
        # Test environment loading
        from dotenv import load_dotenv
        load_dotenv()
        
        import os
        if os.getenv('OANDA_API_KEY'):
            logger.info("✅ Environment variables loaded")
        else:
            logger.warning("⚠️ OANDA_API_KEY not found in environment")
            
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Jarvis Trading Bot - Quick Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        logger.error("❌ Failed to install requirements")
        return False
    
    # Check environment
    env_ok = check_environment_file()
    
    # Run quick test
    if not run_quick_test():
        logger.error("❌ Quick test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    if env_ok:
        print("✅ Your trading bot is ready to run!")
        print("\nNext steps:")
        print("1. Run: python validate_system.py (optional full validation)")
        print("2. Run: python start_trading_bot.py (start the bot)")
        print("3. Open: http://localhost:5000 (dashboard)")
    else:
        print("⚠️ Please configure your .env file with OANDA credentials")
        print("\nRequired .env file contents:")
        print("OANDA_API_KEY=your_api_key_here")
        print("OANDA_ACCOUNT_ID=your_account_id_here") 
        print("OANDA_API_URL=https://api-fxpractice.oanda.com/v3")
        print("OANDA_LIVE=false")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed with error: {e}")
        sys.exit(1)
