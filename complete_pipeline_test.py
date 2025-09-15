#!/usr/bin/env python3
"""
Complete TradingView → Render → OANDA Pipeline Test
Identifies exactly why trades aren't executing
"""

import requests
import json
from datetime import datetime
import time

RENDER_URL = "https://jarvis-quant-sys.onrender.com"

def test_render_basic():
    """Test basic Render connectivity"""
    print("🔍 TESTING RENDER BASIC CONNECTIVITY")
    print("=" * 60)
    
    try:
        response = requests.get(f"{RENDER_URL}/", timeout=30)
        print(f"✅ Render Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Render Connection Failed: {e}")
        return False

def test_webhook_processing():
    """Test webhook with various signal formats"""
    print("\n🎯 TESTING WEBHOOK SIGNAL PROCESSING")
    print("=" * 60)
    
    test_signals = [
        {
            "name": "Basic Test Signal",
            "data": {"test": "pipeline_check", "timestamp": datetime.now().isoformat()}
        },
        {
            "name": "Minimal TradingView Format",
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
                "signal_strength": 45.0,
                "news_bias": -1.0,
                "trend_strength": -7.0,
                "stop_loss": 1.27100,
                "take_profit": 1.26300
            }
        }
    ]
    
    results = []
    for i, test in enumerate(test_signals, 1):
        print(f"\n🔸 Test {i}: {test['name']}")
        
        try:
            response = requests.post(
                f"{RENDER_URL}/webhook",
                json=test['data'],
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Success: {response.text[:150]}")
                results.append("SUCCESS")
            elif response.status_code == 500:
                print(f"   ❌ Server Error: {response.text}")
                results.append("SERVER_ERROR")
            else:
                print(f"   ⚠️  Other Error: {response.status_code} - {response.text[:100]}")
                results.append("OTHER_ERROR")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - Render might be sleeping")
            results.append("TIMEOUT")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results.append("EXCEPTION")
    
    return results

def analyze_error_patterns(results):
    """Analyze error patterns to identify root cause"""
    print("\n🔍 ERROR PATTERN ANALYSIS")
    print("=" * 60)
    
    error_counts = {}
    for result in results:
        error_counts[result] = error_counts.get(result, 0) + 1
    
    print("📊 Result Summary:")
    for error_type, count in error_counts.items():
        print(f"   {error_type}: {count}")
    
    # Diagnose issues
    print("\n🎯 DIAGNOSIS:")
    
    if error_counts.get("SERVER_ERROR", 0) > 0:
        print("❌ OANDA API CONNECTION ISSUE DETECTED")
        print("   • Render deployment can receive webhooks")
        print("   • But fails when trying to connect to OANDA")
        print("   • This suggests:")
        print("     - OANDA credentials missing/incorrect in Render")
        print("     - Latest code not deployed to Render")
        print("     - OANDA API network restrictions")
        return "OANDA_CONNECTION_ISSUE"
    
    elif error_counts.get("TIMEOUT", 0) > 0:
        print("⏰ RENDER COLD START ISSUE")
        print("   • Render free tier sleeps after 15 minutes")
        print("   • Apps take 30-60 seconds to wake up")
        return "COLD_START"
    
    elif error_counts.get("SUCCESS", 0) == len(results):
        print("✅ ALL TESTS PASSED")
        print("   • Pipeline appears functional")
        print("   • Issue might be TradingView alert configuration")
        return "PIPELINE_OK"
    
    else:
        print("❓ MIXED RESULTS - FURTHER INVESTIGATION NEEDED")
        return "MIXED_RESULTS"

def test_oanda_direct():
    """Test OANDA connection directly"""
    print("\n🏦 TESTING OANDA API DIRECT CONNECTION")
    print("=" * 60)
    
    # Test with a status endpoint if it exists
    try:
        response = requests.get(f"{RENDER_URL}/status", timeout=30)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status Endpoint: {status_data}")
            return True
        else:
            print(f"⚠️  Status endpoint returned: {response.status_code}")
    except:
        print("⚠️  No status endpoint available")
    
    # Test with account check endpoint if it exists
    try:
        response = requests.get(f"{RENDER_URL}/account", timeout=30)
        if response.status_code == 200:
            account_data = response.json()
            print(f"✅ Account Endpoint: {account_data}")
            return True
        else:
            print(f"⚠️  Account endpoint: {response.status_code}")
    except:
        print("⚠️  No account endpoint available")
    
    return False

def provide_solutions(diagnosis):
    """Provide specific solutions based on diagnosis"""
    print("\n🛠️  RECOMMENDED SOLUTIONS")
    print("=" * 60)
    
    if diagnosis == "OANDA_CONNECTION_ISSUE":
        print("🎯 OANDA CONNECTION FIXES:")
        print()
        print("1. CHECK RENDER ENVIRONMENT VARIABLES:")
        print("   • Go to Render Dashboard → Your Service → Environment")
        print("   • Ensure these are set:")
        print("     - OANDA_API_KEY")
        print("     - OANDA_ACCOUNT_ID") 
        print("     - OANDA_API_URL")
        print()
        print("2. REDEPLOY LATEST CODE:")
        print("   • Your latest code changes might not be on Render")
        print("   • Commit and push all changes to trigger redeploy")
        print()
        print("3. CHECK OANDA API STATUS:")
        print("   • Verify OANDA Live API is accessible")
        print("   • Test API key hasn't expired")
        print()
        print("🚀 IMMEDIATE ACTION:")
        print("   Run this to force Render redeploy:")
        print("   git commit -m 'Force redeploy' --allow-empty && git push")
        
    elif diagnosis == "COLD_START":
        print("⏰ COLD START SOLUTIONS:")
        print()
        print("1. PING RENDER REGULARLY:")
        print("   • Set up a cron job or monitoring service")
        print("   • Ping your Render URL every 10-15 minutes")
        print()
        print("2. UPGRADE TO PAID RENDER PLAN:")
        print("   • Paid plans don't have cold start delays")
        print("   • Always stay warm and responsive")
        print()
        print("🚀 IMMEDIATE ACTION:")
        print("   Wait 60 seconds and retry tests")
        
    elif diagnosis == "PIPELINE_OK":
        print("✅ PIPELINE IS WORKING - CHECK TRADINGVIEW:")
        print()
        print("1. VERIFY TRADINGVIEW ALERT:")
        print("   • Check alert is active (green dot)")
        print("   • Verify webhook URL is correct")
        print("   • Ensure alert hasn't been paused")
        print()
        print("2. CHECK SIGNAL CONDITIONS:")
        print("   • Lower minSignalStrength to 20.0 temporarily")
        print("   • Set news_bias to match market sentiment")
        print("   • Verify trading session times")
        print()
        print("🚀 IMMEDIATE ACTION:")
        print("   Monitor TradingView alerts list for activity")
    
    else:
        print("🔍 MIXED RESULTS - COMPREHENSIVE CHECK:")
        print()
        print("1. CHECK RENDER LOGS:")
        print("   • Go to Render Dashboard → Logs")
        print("   • Look for webhook processing messages")
        print("   • Check for error patterns")
        print()
        print("2. VERIFY CODE DEPLOYMENT:")
        print("   • Ensure latest commits are deployed")
        print("   • Check environment variables")
        print()
        print("🚀 IMMEDIATE ACTION:")
        print("   Check Render deployment logs for detailed errors")

def main():
    """Run complete pipeline diagnostic"""
    print("🚀 COMPLETE TRADINGVIEW → RENDER → OANDA PIPELINE TEST")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Target: {RENDER_URL}")
    
    # Test basic connectivity
    basic_ok = test_render_basic()
    
    if not basic_ok:
        print("\n❌ BASIC CONNECTIVITY FAILED - CHECK RENDER DEPLOYMENT")
        return
    
    # Test webhook processing
    results = test_webhook_processing()
    
    # Analyze patterns
    diagnosis = analyze_error_patterns(results)
    
    # Test OANDA if possible
    test_oanda_direct()
    
    # Provide solutions
    provide_solutions(diagnosis)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL DIAGNOSIS")
    print("=" * 60)
    
    print(f"🎯 Issue Type: {diagnosis}")
    print(f"📡 Webhook URL: {RENDER_URL}/webhook")
    
    if diagnosis == "OANDA_CONNECTION_ISSUE":
        print("🔧 Next Step: Fix OANDA connection on Render")
    elif diagnosis == "COLD_START":
        print("⏰ Next Step: Wait for warm-up or upgrade Render plan")
    elif diagnosis == "PIPELINE_OK":
        print("✅ Next Step: Check TradingView alert configuration")
    else:
        print("🔍 Next Step: Check Render logs for detailed errors")

if __name__ == "__main__":
    main()
