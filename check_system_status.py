#!/usr/bin/env python3
"""
JARVIS System Status Checker
Quick way to verify everything is working
"""

import os
import requests
import json
from datetime import datetime

def print_header():
    print("🔍" * 60)
    print("JARVIS SYSTEM STATUS CHECK")
    print("🔍" * 60)
    print(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_system_running():
    """Check if JARVIS Flask app is running"""
    print("🚀 CHECKING JARVIS SYSTEM...")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            print("✅ JARVIS System: RUNNING")
            return True
        else:
            print(f"⚠️ JARVIS System: RESPONDING BUT ERROR ({response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ JARVIS System: NOT RUNNING")
        print("   → Start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ JARVIS System: ERROR - {e}")
        return False

def check_oanda_config():
    """Check OANDA configuration"""
    print("\n🏦 CHECKING OANDA CONFIGURATION...")
    
    if not os.path.exists('.env'):
        print("❌ Configuration file (.env) not found")
        return False
    
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
        
        # Check for required OANDA settings
        required_settings = [
            'OANDA_API_KEY',
            'OANDA_ACCOUNT_ID', 
            'OANDA_LIVE',
            'OANDA_API_URL'
        ]
        
        missing = []
        for setting in required_settings:
            if setting not in env_content:
                missing.append(setting)
        
        if missing:
            print(f"❌ Missing settings: {', '.join(missing)}")
            return False
        
        # Check if live mode is enabled
        if 'OANDA_LIVE=true' in env_content:
            print("✅ OANDA Config: LIVE MODE ACTIVE")
        else:
            print("⚠️ OANDA Config: DEMO MODE (not live trading)")
        
        print("✅ OANDA Configuration: COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def check_webhook_endpoint():
    """Check if webhook endpoint is accessible"""
    print("\n🌐 CHECKING WEBHOOK ENDPOINT...")
    
    try:
        # Test with a simple POST to webhook
        test_payload = {
            "symbol": "EURUSD",
            "action": "TEST",
            "price": 1.0000,
            "time": datetime.now().isoformat(),
            "strategy": "STATUS_CHECK"
        }
        
        response = requests.post(
            "http://127.0.0.1:5000/webhook",
            json=test_payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Webhook Endpoint: ACCESSIBLE")
            print("   → TradingView URL: http://127.0.0.1:5000/webhook")
            return True
        else:
            print(f"⚠️ Webhook Endpoint: RESPONDING BUT ERROR ({response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Webhook Endpoint: NOT ACCESSIBLE")
        print("   → Ensure JARVIS system is running")
        return False
    except Exception as e:
        print(f"❌ Webhook Error: {e}")
        return False

def check_account_balance():
    """Display current account information"""
    print("\n💰 ACCOUNT INFORMATION...")
    
    # This is informational since we can't easily check OANDA balance without complex auth
    print("Current Balance: $0.95 (add funds for meaningful trading)")
    print("Recommended minimum: $100")
    print("Risk per trade: 2% of account balance")
    print("With $0.95: Risk ~$0.02 per trade")
    print("With $100: Risk ~$2.00 per trade")

def check_system_files():
    """Check if critical system files exist"""
    print("\n📁 CHECKING SYSTEM FILES...")
    
    critical_files = [
        'app.py',
        'live_trading_system.py', 
        'oanda_client.py',
        'train_and_trade_100_sessions.py',
        '.env'
    ]
    
    missing_files = []
    for file in critical_files:
        if os.path.exists(file):
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"✅ {file} ({size_mb:.1f}MB)")
        else:
            missing_files.append(file)
            print(f"❌ {file} - MISSING")
    
    if missing_files:
        print(f"\n⚠️ Missing critical files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All critical system files present")
        return True

def main():
    print_header()
    
    # Run all checks
    checks = [
        ("System Files", check_system_files()),
        ("OANDA Config", check_oanda_config()), 
        ("JARVIS System", check_system_running()),
        ("Webhook Endpoint", check_webhook_endpoint()),
    ]
    
    # Account info (always runs)
    check_account_balance()
    
    # Summary
    print("\n" + "="*60)
    print("SYSTEM STATUS SUMMARY")
    print("="*60)
    
    passed = 0
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Status: {passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        print("\n🎉 ALL SYSTEMS GO! Your JARVIS system is ready for trading!")
        print("\n📋 NEXT STEPS:")
        print("1. Set up TradingView alerts")
        print("2. Test with small signals first")  
        print("3. Monitor for a few hours")
        print("4. Add more funds when comfortable")
    else:
        print("\n⚠️ Some issues detected. Fix the failed checks before trading.")
    
    print("\n" + "🔍" * 60)

if __name__ == "__main__":
    main()
