#!/usr/bin/env python3
"""
SevenSYS Complete System Diagnostic
Tests all components to identify why no trade signals are being generated
"""

import json
import requests
import sys
from datetime import datetime
import sqlite3
import os

def test_flask_webhook():
    """Test if Flask webhook is responding"""
    print("=" * 60)
    print("1. TESTING FLASK WEBHOOK SERVER")
    print("=" * 60)
    
    try:
        # Test basic ping
        response = requests.post(
            'http://localhost:5000/webhook',
            json={'test': 'diagnostic_ping'},
            timeout=5
        )
        print(f"✅ Flask webhook responding: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Flask webhook server not responding")
        print("   ACTION NEEDED: Start Flask app with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def test_oanda_connection():
    """Test OANDA API connection"""
    print("\n" + "=" * 60)
    print("2. TESTING OANDA API CONNECTION")
    print("=" * 60)
    
    try:
        from config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_API_URL
        import oandapyV20
        from oandapyV20 import API
        from oandapyV20.endpoints import accounts
        
        # Test API connection
        api = API(access_token=OANDA_API_KEY, environment="live")
        
        # Get account info
        account_ep = accounts.AccountDetails(accountID=OANDA_ACCOUNT_ID)
        response = api.request(account_ep)
        
        account = response['account']
        balance = float(account['balance'])
        nav = float(account['NAV'])
        
        print(f"✅ OANDA API connected successfully")
        print(f"   Account ID: {OANDA_ACCOUNT_ID}")
        print(f"   Balance: ${balance:,.2f}")
        print(f"   NAV: ${nav:,.2f}")
        print(f"   Margin Available: ${float(account.get('marginAvailable', 0)):,.2f}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing OANDA dependencies: {e}")
        print("   ACTION NEEDED: pip install oandapyV20")
        return False
    except Exception as e:
        print(f"❌ OANDA connection failed: {e}")
        print("   ACTION NEEDED: Check OANDA credentials in config.py")
        return False

def test_webhook_simulation():
    """Test webhook with realistic TradingView data"""
    print("\n" + "=" * 60)
    print("3. TESTING WEBHOOK WITH SIMULATED TRADINGVIEW DATA")
    print("=" * 60)
    
    # Realistic TradingView webhook data
    test_signals = [
        {
            "ticker": "EUR_USD",
            "strategy.order.action": "buy",
            "close": 1.08500,
            "strategy": "SevenSYS",
            "signal_strength": 45.0,
            "news_bias": 5.0,
            "trend_strength": 8.0,
            "stop_loss": 1.08200,
            "take_profit": 1.09000
        },
        {
            "ticker": "GBP_USD", 
            "strategy.order.action": "sell",
            "close": 1.26800,
            "strategy": "SevenSYS",
            "signal_strength": 42.0,
            "news_bias": -3.0,
            "trend_strength": -6.0,
            "stop_loss": 1.27100,
            "take_profit": 1.26300
        }
    ]
    
    success_count = 0
    for i, signal in enumerate(test_signals, 1):
        try:
            print(f"\nTesting signal {i}: {signal['strategy.order.action'].upper()} {signal['ticker']}")
            
            response = requests.post(
                'http://localhost:5000/webhook',
                json=signal,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Signal {i} processed successfully")
                print(f"   Response: {response.text[:150]}")
                success_count += 1
            else:
                print(f"❌ Signal {i} failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Signal {i} error: {e}")
    
    print(f"\n📊 Webhook simulation results: {success_count}/{len(test_signals)} successful")
    return success_count > 0

def check_memory_database():
    """Check trading memory database"""
    print("\n" + "=" * 60)
    print("4. CHECKING TRADING MEMORY DATABASE")
    print("=" * 60)
    
    try:
        if not os.path.exists('sevensys_memory.db'):
            print("❌ Memory database not found")
            print("   ACTION NEEDED: Database will be created on first trade")
            return False
            
        conn = sqlite3.connect('sevensys_memory.db')
        cursor = conn.cursor()
        
        # Check recent trades
        cursor.execute("""
            SELECT COUNT(*) as trade_count, 
                   MAX(timestamp) as last_trade,
                   AVG(CASE WHEN profit_loss > 0 THEN 1.0 ELSE 0.0 END) as win_rate
            FROM trades 
            WHERE timestamp > datetime('now', '-24 hours')
        """)
        
        result = cursor.fetchone()
        trade_count, last_trade, win_rate = result
        
        print(f"✅ Memory database operational")
        print(f"   Trades (last 24h): {trade_count}")
        print(f"   Last trade: {last_trade or 'None'}")
        if win_rate is not None:
            print(f"   Win rate: {win_rate*100:.1f}%")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Memory database error: {e}")
        return False

def analyze_pine_script_conditions():
    """Analyze why SevenSYS might not be generating signals"""
    print("\n" + "=" * 60)
    print("5. ANALYZING PINE SCRIPT SIGNAL CONDITIONS")
    print("=" * 60)
    
    print("📋 SevenSYS Signal Requirements Analysis:")
    print("   ├─ Minimum Signal Strength: 35.0 (default)")
    print("   ├─ Trend Requirements:")
    print("   │  ├─ LONG: trend_strength > 0.5, close > EMA21, HTF bullish")
    print("   │  └─ SHORT: trend_strength < -0.5, close < EMA21, HTF bearish")
    print("   ├─ Momentum Requirements:")
    print("   │  ├─ LONG: momentum_score > -5.0, RSI > 40 OR bullish RSI")
    print("   │  └─ SHORT: momentum_score < 5.0, RSI < 60 OR bearish RSI")
    print("   ├─ Session Requirements: London, NY, or Asian sessions")
    print("   ├─ Market Conditions: Trending or Ranging (NOT choppy)")
    print("   └─ News Filter: Allows trades based on news_bias")
    
    print("\n🔍 Common reasons for no signals:")
    print("   ❯ Signal strength below 35.0 threshold")
    print("   ❯ Choppy market conditions (high volatility + weak trend)")
    print("   ❯ Outside active trading sessions")
    print("   ❯ News filter blocking trades")
    print("   ❯ Safety systems activated (drawdown limits)")
    print("   ❯ No TradingView alerts configured")
    
    print("\n⚡ CRITICAL CHECK: Are TradingView alerts set up?")
    print("   URL needed: http://localhost:5000/webhook")
    print("   Message format: {{\"ticker\": \"{{ticker}}\", \"strategy.order.action\": \"{{strategy.order.action}}\", \"close\": {{close}}}}")
    
    return True

def check_news_system():
    """Check news monitoring system"""
    print("\n" + "=" * 60)
    print("6. CHECKING NEWS MONITORING SYSTEM")
    print("=" * 60)
    
    try:
        if os.path.exists('sevensys_news_settings.json'):
            with open('sevensys_news_settings.json', 'r') as f:
                settings = json.load(f)
            print(f"✅ News settings found")
            print(f"   News bias: {settings.get('news_bias', 0.0)}")
            print(f"   Auto update: {settings.get('auto_news_update', False)}")
        else:
            print("⚠️  News settings file not found")
            print("   Using default news_bias: 0.0")
        
        return True
    except Exception as e:
        print(f"❌ News system error: {e}")
        return False

def generate_recommendations():
    """Generate action recommendations"""
    print("\n" + "=" * 60)
    print("7. DIAGNOSTIC RECOMMENDATIONS")
    print("=" * 60)
    
    print("🎯 IMMEDIATE ACTIONS TO GET SIGNALS:")
    print()
    print("1. VERIFY TRADINGVIEW SETUP:")
    print("   ├─ Open TradingView with SevenSYS_Complete.pine")
    print("   ├─ Set up alerts with webhook URL: http://localhost:5000/webhook")
    print("   ├─ Use message: {{\"ticker\":\"{{ticker}}\",\"strategy.order.action\":\"{{strategy.order.action}}\",\"close\":{{close}}}}")
    print("   └─ Ensure alerts are active and firing")
    print()
    print("2. ADJUST SIGNAL SENSITIVITY:")
    print("   ├─ Lower minSignalStrength from 35.0 to 25.0")
    print("   ├─ Set news_bias to match current market sentiment")
    print("   └─ Consider disabling major_event_mode if enabled")
    print()
    print("3. CHECK MARKET CONDITIONS:")
    print("   ├─ Ensure trading during London/NY sessions")
    print("   ├─ Verify market isn't too choppy/volatile")
    print("   └─ Check that safety systems aren't blocking trades")
    print()
    print("4. MONITOR SYSTEM LOGS:")
    print("   ├─ Watch Flask terminal for incoming webhooks")
    print("   ├─ Check memory_logger.log for trade attempts")
    print("   └─ Verify OANDA order placement")

def main():
    """Run complete system diagnostic"""
    print("🔧 SEVENSYS COMPLETE SYSTEM DIAGNOSTIC")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'flask_webhook': test_flask_webhook(),
        'oanda_connection': test_oanda_connection(), 
        'webhook_simulation': test_webhook_simulation(),
        'memory_database': check_memory_database(),
        'pine_script_analysis': analyze_pine_script_conditions(),
        'news_system': check_news_system()
    }
    
    generate_recommendations()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall System Health: {passed}/{total} components operational")
    
    if passed == total:
        print("🚀 System fully operational - signals should be generating!")
    elif passed >= 4:
        print("⚠️  System mostly operational - check TradingView alerts")
    else:
        print("🔴 System needs attention - fix critical issues first")

if __name__ == "__main__":
    main()
