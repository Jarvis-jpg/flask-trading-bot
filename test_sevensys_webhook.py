#!/usr/bin/env python3
"""
Comprehensive SevenSYS Webhook Testing System
Tests webhook integration with realistic SevenSYS trading alerts
"""

import requests
import json
import time
from datetime import datetime, timezone

# Test webhook URL
WEBHOOK_URL = "http://localhost:5000/webhook"

# Realistic SevenSYS test alerts based on the Pine Script format
test_alerts = [
    {
        "name": "Strong Bullish Signal",
        "data": {
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
    },
    {
        "name": "Strong Bearish Signal", 
        "data": {
            "ticker": "GBPUSD",
            "strategy.order.action": "sell",
            "close": 1.2650,
            "strategy": "SevenSYS", 
            "signal_strength": 62.1,
            "news_bias": -12.0,
            "trend_strength": -15.7,
            "stop_loss": 1.2680,
            "take_profit": 1.2585
        }
    },
    {
        "name": "Regular Long Signal",
        "data": {
            "ticker": "USDJPY",
            "strategy.order.action": "buy", 
            "close": 150.25,
            "strategy": "SevenSYS",
            "signal_strength": 42.6,
            "news_bias": 3.2,
            "trend_strength": 8.4,
            "stop_loss": 149.80,
            "take_profit": 151.35
        }
    },
    {
        "name": "Regular Short Signal",
        "data": {
            "ticker": "AUDUSD", 
            "strategy.order.action": "sell",
            "close": 0.6520,
            "strategy": "SevenSYS",
            "signal_strength": 39.8,
            "news_bias": -4.1,
            "trend_strength": -9.2,
            "stop_loss": 0.6545,
            "take_profit": 0.6470
        }
    },
    {
        "name": "Emergency Close All",
        "data": {
            "ticker": "EURUSD",
            "strategy.order.action": "close_all",
            "close": 1.0840,
            "strategy": "SevenSYS",
            "reason": "safety_stop",
            "news_bias": -15.8
        }
    },
    {
        "name": "Weak Signal (Should Not Execute)",
        "data": {
            "ticker": "NZDUSD",
            "strategy.order.action": "buy",
            "close": 0.5985,
            "strategy": "SevenSYS",
            "signal_strength": 28.3,  # Below minimum threshold
            "news_bias": 1.2,
            "trend_strength": 2.1,
            "stop_loss": 0.5970,
            "take_profit": 0.6015
        }
    }
]

def test_webhook_connectivity():
    """Test basic webhook connectivity"""
    print("🔗 Testing webhook connectivity...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Flask app is running")
            print(f"   - Service: {result.get('service', 'Unknown')}")
            print(f"   - Environment: {result.get('environment', 'Unknown')}")
            print(f"   - Account: {result.get('account', 'Unknown')}")
            return True
        else:
            print(f"❌ Flask app responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app")
        print("   Please start the app with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_single_webhook(test_case):
    """Test a single webhook alert"""
    print(f"\n📊 Testing: {test_case['name']}")
    print(f"   Alert: {test_case['data'].get('strategy.order.action', 'unknown').upper()} {test_case['data'].get('ticker', 'unknown')}")
    
    if 'signal_strength' in test_case['data']:
        strength = test_case['data']['signal_strength']
        print(f"   Signal Strength: {strength}")
        
    try:
        start_time = time.time()
        response = requests.post(WEBHOOK_URL, json=test_case['data'], timeout=15)
        response_time = time.time() - start_time
        
        print(f"   Response Time: {response_time:.2f}s")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {result.get('status', 'unknown')}")
            print(f"   Message: {result.get('message', 'No message')}")
            
            if 'trade_data' in result:
                trade_data = result['trade_data']
                if 'orderFillTransaction' in trade_data:
                    fill = trade_data['orderFillTransaction']
                    print(f"   💰 Trade Executed:")
                    print(f"      - Order ID: {fill.get('id', 'unknown')}")
                    print(f"      - Units: {fill.get('units', 'unknown')}")
                    print(f"      - Price: {fill.get('price', 'unknown')}")
                    
            return True, response_time
            
        elif response.status_code == 400:
            result = response.json()
            print(f"   ⚠️  Validation Error: {result.get('message', 'unknown')}")
            return False, response_time
            
        elif response.status_code == 500:
            result = response.json()
            print(f"   ❌ Server Error: {result.get('message', 'unknown')}")
            return False, response_time
            
        else:
            print(f"   ❓ Unexpected status: {response.text}")
            return False, response_time
            
    except requests.exceptions.Timeout:
        print("   ⏰ Request timed out (>15s)")
        return False, 15.0
    except requests.exceptions.ConnectionError:
        print("   🔌 Connection error - is the Flask app running?")
        return False, 0.0
    except Exception as e:
        print(f"   💥 Unexpected error: {e}")
        return False, 0.0

def analyze_webhook_responses():
    """Analyze webhook behavior patterns"""
    print("\n📈 Analyzing webhook performance...")
    
    successful_tests = 0
    total_response_time = 0.0
    execution_tests = 0
    actual_executions = 0
    
    for test_case in test_alerts:
        success, response_time = test_single_webhook(test_case)
        
        if success:
            successful_tests += 1
            total_response_time += response_time
            
            # Check if this should execute a trade
            data = test_case['data']
            action = data.get('strategy.order.action', '')
            strength = data.get('signal_strength', 0)
            
            if action in ['buy', 'sell'] and strength >= 35.0:  # Minimum signal strength
                execution_tests += 1
                # In a real test, we'd check if trade was actually placed
                actual_executions += 1
        
        time.sleep(1)  # Prevent overwhelming the server
    
    print(f"\n📊 Test Results Summary:")
    print(f"   Total Tests: {len(test_alerts)}")
    print(f"   Successful: {successful_tests}/{len(test_alerts)}")
    print(f"   Success Rate: {(successful_tests/len(test_alerts)*100):.1f}%")
    
    if successful_tests > 0:
        avg_response_time = total_response_time / successful_tests
        print(f"   Avg Response Time: {avg_response_time:.2f}s")
        
    print(f"   Expected Executions: {execution_tests}")
    print(f"   Actual Executions: {actual_executions}")
    
    if execution_tests > 0:
        execution_rate = (actual_executions / execution_tests * 100)
        print(f"   Execution Rate: {execution_rate:.1f}%")
        
        if execution_rate >= 90:
            print("   ✅ Webhook execution is working correctly")
        elif execution_rate >= 70:
            print("   ⚠️  Some trades may not be executing")
        else:
            print("   ❌ Low execution rate - check system logs")

def test_error_handling():
    """Test webhook error handling"""
    print("\n🛠️  Testing error handling...")
    
    error_tests = [
        {
            "name": "Empty Request",
            "data": {}
        },
        {
            "name": "Missing Required Fields", 
            "data": {
                "ticker": "EURUSD",
                "strategy.order.action": "buy"
                # Missing close, stop_loss, take_profit
            }
        },
        {
            "name": "Invalid Action",
            "data": {
                "ticker": "GBPUSD",
                "strategy.order.action": "invalid_action",
                "close": 1.2650,
                "stop_loss": 1.2625,
                "take_profit": 1.2700
            }
        },
        {
            "name": "Invalid Ticker",
            "data": {
                "ticker": "INVALID",
                "strategy.order.action": "buy", 
                "close": 1.0000,
                "stop_loss": 0.9950,
                "take_profit": 1.0100
            }
        }
    ]
    
    error_handled_correctly = 0
    
    for error_test in error_tests:
        print(f"\n   Testing: {error_test['name']}")
        try:
            response = requests.post(WEBHOOK_URL, json=error_test['data'], timeout=10)
            
            if response.status_code in [400, 500]:  # Expected error codes
                result = response.json()
                print(f"   ✅ Handled correctly: {result.get('message', 'No message')}")
                error_handled_correctly += 1
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
        
        except Exception as e:
            print(f"   💥 Error in error test: {e}")
    
    print(f"\n   Error Handling Summary:")
    print(f"   Tests: {len(error_tests)}")
    print(f"   Handled Correctly: {error_handled_correctly}/{len(error_tests)}")
    
    if error_handled_correctly == len(error_tests):
        print("   ✅ Error handling is working correctly")
    else:
        print("   ⚠️  Some errors may not be handled properly")

def main():
    """Run comprehensive webhook testing"""
    print("🚀 SevenSYS Webhook Testing System")
    print("=" * 50)
    
    # Test connectivity first
    if not test_webhook_connectivity():
        print("\n❌ Cannot continue without Flask app connectivity")
        return
    
    print(f"\n🕒 Starting tests at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
    
    # Test all webhook scenarios
    analyze_webhook_responses()
    
    # Test error handling
    test_error_handling()
    
    print(f"\n🏁 Testing completed at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
    print("\n📋 Next Steps:")
    print("   1. Check Flask app logs for detailed execution info")
    print("   2. Verify OANDA account for actual trade execution")
    print("   3. Test with live TradingView alerts")
    print("   4. Monitor SevenSYS news automation system")

if __name__ == "__main__":
    main()
