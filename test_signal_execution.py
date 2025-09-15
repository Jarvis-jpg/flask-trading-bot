#!/usr/bin/env python3
"""
Direct Trading Signal Test
Sends realistic webhook data to test signal processing
"""

import requests
import json
from datetime import datetime

def test_trading_signals():
    """Test webhook with various realistic trading scenarios"""
    
    print("🚀 TESTING SEVENSYS WEBHOOK WITH REALISTIC SIGNALS")
    print("=" * 60)
    
    # Test signals with different strengths and conditions
    test_signals = [
        {
            "name": "Strong BUY Signal - EUR/USD",
            "data": {
                "ticker": "EUR_USD",
                "strategy.order.action": "buy",
                "close": 1.08500,
                "strategy": "SevenSYS",
                "signal_strength": 48.5,
                "news_bias": 3.0,
                "trend_strength": 12.0,
                "stop_loss": 1.08200,
                "take_profit": 1.09000
            }
        },
        {
            "name": "Medium SELL Signal - GBP/USD", 
            "data": {
                "ticker": "GBP_USD",
                "strategy.order.action": "sell", 
                "close": 1.26800,
                "strategy": "SevenSYS",
                "signal_strength": 38.2,
                "news_bias": -2.0,
                "trend_strength": -8.5,
                "stop_loss": 1.27100,
                "take_profit": 1.26300
            }
        },
        {
            "name": "Weak Signal Test - USD/JPY",
            "data": {
                "ticker": "USD_JPY",
                "strategy.order.action": "buy",
                "close": 148.50,
                "strategy": "SevenSYS", 
                "signal_strength": 25.0,  # Below default threshold
                "news_bias": 0.0,
                "trend_strength": 3.0,
                "stop_loss": 148.00,
                "take_profit": 149.50
            }
        }
    ]
    
    webhook_url = "http://localhost:5000/webhook"
    results = []
    
    for i, test in enumerate(test_signals, 1):
        print(f"\n📡 Test {i}: {test['name']}")
        print(f"   Signal Strength: {test['data']['signal_strength']}")
        print(f"   Action: {test['data']['strategy.order.action'].upper()}")
        
        try:
            response = requests.post(
                webhook_url,
                json=test['data'],
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
            if response.status_code == 200:
                if "trade executed" in response.text.lower():
                    print("   ✅ TRADE EXECUTED!")
                    results.append("✅ EXECUTED")
                elif "processed" in response.text.lower():
                    print("   ⚠️  Signal processed but no trade")
                    results.append("⚠️ PROCESSED") 
                else:
                    print("   ❓ Unknown response")
                    results.append("❓ UNKNOWN")
            else:
                print("   ❌ Failed to process")
                results.append("❌ FAILED")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection failed - Flask app not running?")
            results.append("❌ NO CONNECTION")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append("❌ ERROR")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for i, (test, result) in enumerate(zip(test_signals, results), 1):
        print(f"{result} Test {i}: {test['name']}")
    
    executed_count = sum(1 for r in results if "EXECUTED" in r)
    print(f"\n🎯 Trades Executed: {executed_count}/{len(test_signals)}")
    
    if executed_count == 0:
        print("\n🔍 NO TRADES EXECUTED - POSSIBLE CAUSES:")
        print("   ├─ Signal strength below threshold (default: 35.0)")
        print("   ├─ OANDA API connection issues") 
        print("   ├─ Insufficient account balance")
        print("   ├─ Safety systems blocking trades")
        print("   ├─ Market conditions not suitable")
        print("   └─ Configuration issues")
        
        print("\n⚡ NEXT STEPS:")
        print("   1. Check Flask terminal for error messages")
        print("   2. Verify OANDA account has sufficient balance")
        print("   3. Check if safety systems are activated")
        print("   4. Consider lowering signal strength threshold")
    else:
        print(f"\n🚀 SUCCESS! System is executing trades!")

if __name__ == "__main__":
    test_trading_signals()
