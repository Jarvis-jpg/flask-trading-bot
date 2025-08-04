#!/usr/bin/env python3
"""
JARVIS System Verification Script
Verifies all components are working correctly for deployment
"""

import os
import sys
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def check_environment():
    """Check environment configuration"""
    print_header("🔍 ENVIRONMENT VERIFICATION")
    
    load_dotenv()
    
    required_vars = [
        ('OANDA_API_KEY', 'OANDA API Key'),
        ('OANDA_ACCOUNT_ID', 'OANDA Account ID'),
        ('OANDA_API_URL', 'OANDA API URL'),
        ('OANDA_LIVE', 'Trading Mode'),
        ('FLASK_ENV', 'Flask Environment')
    ]
    
    all_good = True
    for var, description in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive information
            if 'KEY' in var or 'TOKEN' in var:
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "****"
            else:
                display_value = value
            print(f"✅ {description}: {display_value}")
        else:
            print(f"❌ {description}: NOT SET")
            all_good = False
    
    # Special check for live mode
    is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
    mode = "LIVE" if is_live else "PRACTICE"
    print(f"\n🎯 Trading Mode: {mode}")
    if is_live:
        print("⚠️  WARNING: System configured for LIVE trading with real money!")
    else:
        print("✅ PRACTICE mode - Safe for testing")
    
    return all_good

def check_files():
    """Check if all required files exist"""
    print_header("📁 FILE VERIFICATION")
    
    required_files = [
        ('app.py', 'Flask Application'),
        ('.env', 'Environment Variables'),
        ('requirements.txt', 'Python Dependencies'),
        ('Procfile', 'Deployment Configuration'),
        ('live_trading_system.py', 'Live Trading System'),
        ('oanda_client.py', 'OANDA Client'),
        ('trade_analyzer.py', 'Trade Analyzer'),
        ('autonomous_trading_engine.py', 'Autonomous Engine')
    ]
    
    all_good = True
    for filename, description in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {description}: {filename} ({size:,} bytes)")
        else:
            print(f"❌ {description}: {filename} - NOT FOUND")
            all_good = False
    
    return all_good

def check_python_packages():
    """Check if required Python packages are installed"""
    print_header("📦 PACKAGE VERIFICATION")
    
    required_packages = [
        ('flask', 'flask'),
        ('python-dotenv', 'dotenv'),
        ('oandapyV20', 'oandapyV20'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scikit-learn', 'sklearn'),
        ('gunicorn', 'gunicorn')
    ]
    
    all_good = True
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}: Installed")
        except ImportError:
            print(f"❌ {package_name}: NOT INSTALLED")
            all_good = False
    
    return all_good

def test_oanda_connection():
    """Test OANDA API connection"""
    print_header("🌐 OANDA CONNECTION TEST")
    
    try:
        from oanda_client import OandaClient
        oanda = OandaClient()
        
        # Test account info
        print("🔍 Testing account information...")
        account_info = oanda.get_account_info()
        if account_info:
            print(f"✅ Account ID: {account_info.get('id', 'Unknown')}")
            print(f"✅ Balance: ${account_info.get('balance', 'Unknown')}")
            print(f"✅ Currency: {account_info.get('currency', 'Unknown')}")
        else:
            print("❌ Failed to get account information")
            return False
        
        # Test price data
        print("🔍 Testing price data...")
        price = oanda.get_current_price('EUR_USD')
        if price:
            print(f"✅ EUR/USD Bid: {price.get('bid', 'Unknown')}")
            print(f"✅ EUR/USD Ask: {price.get('ask', 'Unknown')}")
        else:
            print("❌ Failed to get price data")
            return False
        
        print("✅ OANDA connection successful")
        return True
        
    except Exception as e:
        print(f"❌ OANDA connection failed: {e}")
        return False

def test_flask_app():
    """Test if Flask app can start"""
    print_header("🌐 FLASK APPLICATION TEST")
    
    try:
        # Import the app
        print("🔍 Testing Flask app import...")
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test app configuration
        print("🔍 Testing app configuration...")
        with app.app_context():
            print(f"✅ App name: {app.name}")
            print(f"✅ Debug mode: {app.debug}")
        
        print("✅ Flask application test successful")
        return True
        
    except Exception as e:
        print(f"❌ Flask application test failed: {e}")
        return False

def test_deployment_readiness():
    """Test if system is ready for deployment"""
    print_header("🚀 DEPLOYMENT READINESS")
    
    checks = [
        ("Environment Variables", check_environment),
        ("Required Files", check_files),
        ("Python Packages", check_python_packages),
        ("OANDA Connection", test_oanda_connection),
        ("Flask Application", test_flask_app)
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_function in checks:
        print(f"\n🔍 Running {check_name} check...")
        try:
            result = check_function()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
            results[check_name] = False
            all_passed = False
    
    print_header("📊 VERIFICATION SUMMARY")
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n{'🎉 SYSTEM READY FOR DEPLOYMENT' if all_passed else '❌ SYSTEM NOT READY - FIX ISSUES ABOVE'}")
    
    if all_passed:
        is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
        if is_live:
            print("\n⚠️  IMPORTANT REMINDERS FOR LIVE TRADING:")
            print("   • Real money will be used")
            print("   • Monitor the system closely")
            print("   • Set appropriate risk limits")
            print("   • Have a plan to stop trading if needed")
        
        print("\n🚀 DEPLOYMENT COMMANDS:")
        print("   Local: python app.py")
        print("   Production: gunicorn app:app")
        print("   Render: Automatically uses Procfile")
    
    return all_passed

def main():
    """Main verification function"""
    print("🤖 JARVIS System Verification")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        ready = test_deployment_readiness()
        sys.exit(0 if ready else 1)
        
    except KeyboardInterrupt:
        print("\n👋 Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Critical error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
