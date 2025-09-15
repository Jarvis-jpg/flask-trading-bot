#!/usr/bin/env python3
"""
Render Flask App Diagnostic Test
Tests the deployed SevenSYS trading system on Render
"""

import requests
import json
from datetime import datetime
import time

RENDER_URL = "https://jarvis-quant-sys.onrender.com"
WEBHOOK_URL = f"{RENDER_URL}/webhook"

def test_render_deployment():
    """Test if Render deployment is online and responsive"""
    print("🔧 TESTING RENDER DEPLOYMENT")
    print("=" * 60)
    
    try:
        # Test basic connectivity
        print("📡 Testing basic connectivity...")
        response = requests.get(f"{RENDER_URL}/", timeout=15)
        print(f"✅ Render app is online: {response.status_code}")
        
        # Test status endpoint if exists
        try:
            status_response = requests.get(f"{RENDER_URL}/status", timeout=10)
            if status_response.status_code == 200:
                print(f"✅ Status endpoint: {status_response.json()}")
            else:
                print(f"⚠️  Status endpoint: {status_response.status_code}")
        except:
            print("⚠️  No status endpoint found")
            
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Render app timeout - might be sleeping")
        print("   Render free tier sleeps after 15 minutes of inactivity")
        print("   App should wake up in 30-60 seconds...")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Render app")
        print("   Check if deployment is active")
        return False
    except Exception as e:
        print(f"❌ Error testing Render: {e}")
        return False

def test_webhook_endpoint():
    """Test webhook endpoint with realistic trading data"""
    print("\n📡 TESTING WEBHOOK ENDPOINT")
    print("=" * 60)
    
    test_signals = [
        {
            "name": "Basic Connection Test",
            "data": {"test": "ping", "timestamp": datetime.now().isoformat()}
        },
        {
            "name": "TradingView Format Test",
            "data": {
                "ticker": "EUR_USD",
                "strategy.order.action": "buy", 
                "close": 1.08500,
                "strategy": "SevenSYS"
            }
        },
        {
            "name": "Complete SevenSYS Signal",
            "data": {
                "ticker": "GBP_USD",
                "strategy.order.action": "sell",
                "close": 1.26800,
                "strategy": "SevenSYS",
                "signal_strength": 42.0,
                "news_bias": -3.0,
                "trend_strength": -8.0,
                "stop_loss": 1.27100,
                "take_profit": 1.26300
            }
        }
    ]
    
    success_count = 0
    for i, test in enumerate(test_signals, 1):
        print(f"\n🔍 Test {i}: {test['name']}")
        
        try:
            # Add longer timeout for Render
            response = requests.post(
                WEBHOOK_URL,
                json=test['data'],
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Status: {response.status_code}")
            response_text = response.text[:300] + "..." if len(response.text) > 300 else response.text
            print(f"   Response: {response_text}")
            
            if response.status_code == 200:
                success_count += 1
                if "executed" in response.text.lower():
                    print("   🚀 TRADE SIGNAL PROCESSED!")
                elif "processed" in response.text.lower():
                    print("   ✅ Signal received and processed")
                else:
                    print("   ✅ Webhook responding")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("   ❌ Webhook timeout - app might be waking up")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Webhook Test Results: {success_count}/{len(test_signals)} successful")
    return success_count

def check_tradingview_setup():
    """Check TradingView webhook setup requirements"""
    print("\n📋 TRADINGVIEW WEBHOOK SETUP CHECK")
    print("=" * 60)
    
    print("🎯 CRITICAL: TradingView Alert Configuration")
    print(f"   Webhook URL: {WEBHOOK_URL}")
    print("   Message Format:")
    print('   {"ticker": "{{ticker}}", "strategy.order.action": "{{strategy.order.action}}", "close": {{close}}, "strategy": "SevenSYS"}')
    print()
    
    print("⚡ For SevenSYS_Complete.pine alerts:")
    print("   1. Open TradingView with SevenSYS_Complete.pine loaded")
    print("   2. Right-click chart → Add Alert")
    print("   3. Condition: SevenSYS_Complete → Any alert() function call")
    print("   4. Actions → Webhook URL → Paste:", WEBHOOK_URL)
    print("   5. Message → Use the JSON format above")
    print("   6. Save Alert")
    print()
    
    print("🔍 Current SevenSYS Signal Requirements:")
    print("   • Minimum Signal Strength: 35.0 (adjustable)")
    print("   • Active Trading Sessions: London/NY/Asian")
    print("   • Market Conditions: Not choppy/extreme volatility")
    print("   • News Filter: Enabled (news_bias affects signals)")
    print()
    
    print("⚠️  If no signals for hours, consider:")
    print("   • Lower minSignalStrength to 25.0")
    print("   • Set news_bias based on current market sentiment")
    print("   • Check if Major Event Mode is blocking signals")

def wake_up_render():
    """Wake up Render app if it's sleeping"""
    print("\n⏰ WAKING UP RENDER APP")
    print("=" * 60)
    
    print("Sending wake-up requests...")
    for i in range(3):
        try:
            response = requests.get(f"{RENDER_URL}/", timeout=45)
            if response.status_code == 200:
                print(f"✅ App is awake! (attempt {i+1})")
                return True
        except:
            print(f"⏳ Waiting... (attempt {i+1}/3)")
            time.sleep(10)
    
    print("❌ App might be having issues or taking longer to wake up")
    return False

def generate_action_plan():
    """Generate specific action plan for getting signals"""
    print("\n🎯 ACTION PLAN TO GET SIGNALS FLOWING")
    print("=" * 60)
    
    print("1. IMMEDIATE CHECKS:")
    print("   ☐ Verify TradingView has SevenSYS_Complete.pine loaded")
    print(f"   ☐ Confirm alert webhook URL: {WEBHOOK_URL}")
    print("   ☐ Check alert is active and not paused")
    print()
    
    print("2. PINE SCRIPT ADJUSTMENTS (if no signals):")
    print("   ☐ Lower minSignalStrength from 35.0 to 25.0")
    print("   ☐ Set appropriate news_bias for current market")
    print("   ☐ Disable major_event_mode if enabled")
    print()
    
    print("3. RENDER APP MONITORING:")
    print("   ☐ Check Render logs for incoming webhooks")
    print("   ☐ Monitor for webhook processing messages")
    print("   ☐ Verify OANDA trade execution")
    print()
    
    print("4. MARKET CONDITIONS:")
    print("   ☐ Ensure trading during London/NY sessions")
    print("   ☐ Check market isn't too choppy")
    print("   ☐ Verify no safety systems are blocking trades")

def main():
    """Run comprehensive Render deployment test"""
    print("🚀 SEVENSYS RENDER DEPLOYMENT DIAGNOSTIC")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing: {RENDER_URL}")
    
    # Wake up app first if needed
    if not test_render_deployment():
        print("\n⏰ Attempting to wake up Render app...")
        wake_up_render()
    
    # Test webhook functionality
    webhook_success = test_webhook_endpoint()
    
    # Check TradingView setup
    check_tradingview_setup()
    
    # Generate action plan
    generate_action_plan()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if webhook_success >= 2:
        print("🚀 Render deployment is OPERATIONAL!")
        print("   Issue likely: TradingView alerts not configured or signals not triggering")
        print("   Next step: Check TradingView alert setup")
    elif webhook_success >= 1:
        print("⚠️  Render deployment responding but may have issues")
        print("   Next step: Check Render logs for errors")
    else:
        print("🔴 Render deployment issues detected")
        print("   Next step: Check deployment status on Render dashboard")
    
    print(f"\n💡 Main webhook URL to use: {WEBHOOK_URL}")

if __name__ == "__main__":
    main()
