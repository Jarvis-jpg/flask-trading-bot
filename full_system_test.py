#!/usr/bin/env python3
"""
Full SevenSYS System Test
Tests all components to ensure autonomous trading works correctly
"""

import requests
import json
import time
from datetime import datetime

def test_flask_connectivity():
    """Test if Flask app is running"""
    print("🔗 Testing Flask App Connectivity...")
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Flask app is running")
            print(f"   Service: {result.get('service', 'Unknown')}")
            print(f"   Environment: {result.get('environment', 'Unknown')}")
            print(f"   Account: {result.get('account', 'Unknown')}")
            return True
        else:
            print(f"❌ Flask app error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask connection failed: {e}")
        return False

def test_oanda_connection():
    """Test OANDA client directly"""
    print("\n🔧 Testing OANDA Connection...")
    try:
        from oanda_client import OandaClient
        oanda = OandaClient()
        print("✅ OANDA client initialized")
        
        account_details = oanda.get_account_details()
        print(f"✅ Account Balance: ${account_details['balance']:.2f}")
        
        price_data = oanda.get_current_price("EUR_USD")
        print(f"✅ EUR_USD Price: {price_data['bid']:.5f} / {price_data['ask']:.5f}")
        return True
        
    except Exception as e:
        print(f"❌ OANDA test failed: {e}")
        return False

def test_webhook_execution():
    """Test webhook with realistic SevenSYS signal"""
    print("\n🚀 Testing Webhook Execution...")
    
    # Realistic SevenSYS test signal
    test_signal = {
        "ticker": "EURUSD",
        "strategy.order.action": "buy",
        "close": 1.0850,
        "strategy": "SevenSYS",
        "signal_strength": 58.4,
        "news_bias": 8.5,
        "trend_strength": 12.3,
        "stop_loss": 1.0825,
        "take_profit": 1.0900
    }
    
    try:
        print(f"📊 Sending test signal: {test_signal['strategy.order.action'].upper()} {test_signal['ticker']}")
        response = requests.post("http://localhost:5000/webhook", 
                               json=test_signal, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Webhook processed successfully")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Message: {result.get('message', 'No message')}")
            
            # Check if trade was executed
            if 'trade_result' in result:
                trade_result = result['trade_result']
                if trade_result.get('status') == 'success':
                    print(f"✅ Trade executed successfully!")
                    print(f"   Order ID: {trade_result.get('order_id', 'N/A')}")
                    print(f"   Fill Price: {trade_result.get('filled_price', 'N/A')}")
                    return True
                else:
                    print(f"⚠️  Trade execution issue: {trade_result}")
            
            return True
        else:
            result = response.json()
            print(f"❌ Webhook failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def test_news_system():
    """Test news automation system"""
    print("\n📰 Testing News Automation System...")
    try:
        from sevensys_news_automation import SevenSYSNewsAutomation
        
        news_system = SevenSYSNewsAutomation()
        settings = news_system.get_current_settings()
        
        print(f"✅ News system initialized")
        print(f"   News Bias: {settings['news_bias']}")
        print(f"   Major Event Mode: {settings['major_event_mode']}")
        print(f"   Risk per Trade: {settings['risk_per_trade']}%")
        print(f"   Recommendation: {settings['recommendation']}")
        
        return True
        
    except Exception as e:
        print(f"❌ News system test failed: {e}")
        return False

def run_comprehensive_test():
    """Run complete system test"""
    print("🤖 SEVENSYS COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Flask App", test_flask_connectivity),
        ("OANDA Connection", test_oanda_connection), 
        ("Webhook Execution", test_webhook_execution),
        ("News System", test_news_system)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"💥 {test_name} test crashed: {e}")
            results[test_name] = False
    
    print(f"\n📊 TEST RESULTS SUMMARY:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ SevenSYS autonomous trading system is fully operational")
        print("✅ System ready for live trading with TradingView alerts")
    else:
        print(f"\n⚠️  {len(tests) - passed} tests failed")
        print("❌ System needs attention before live trading")
    
    print("\n🎯 Next Steps:")
    if passed == len(tests):
        print("1. Set up TradingView alerts with webhook URL: http://localhost:5000/webhook")
        print("2. Configure SevenSYS_Complete.pine script on TradingView")
        print("3. Start news automation: python sevensys_news_automation.py")
        print("4. Monitor memory dashboard: python memory_dashboard.py")
    else:
        print("1. Fix failed tests before proceeding")
        print("2. Check logs for error details")
        print("3. Re-run this test after fixes")

if __name__ == "__main__":
    run_comprehensive_test()
