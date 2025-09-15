"""
SevenSYS Signal Analysis - Check why no signals are being generated
Analyzes market conditions vs SevenSYS requirements
"""

import requests
import json
from datetime import datetime, timedelta
import logging
from memory_logger import SevenSYSMemoryLogger

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_sevensys_conditions():
    """Analyze why SevenSYS might not be generating signals"""
    
    print("🔍 SEVENSYS SIGNAL ANALYSIS")
    print("=" * 50)
    
    # Check memory logger for recent activity
    memory_logger = SevenSYSMemoryLogger()
    today_summary = memory_logger.get_today_summary()
    system_status = memory_logger.get_system_status()
    
    print(f"📊 TODAY'S ACTIVITY:")
    print(f"  • Total Webhook Alerts: {today_summary.get('total_alerts', 0)}")
    print(f"  • Successful Trades: {today_summary.get('successful_trades', 0)}")
    print(f"  • Failed Trades: {today_summary.get('failed_trades', 0)}")
    print(f"  • Success Rate: {today_summary.get('success_rate', 0):.1f}%")
    
    print(f"\n🖥️ SYSTEM STATUS:")
    print(f"  • Total Historical Alerts: {system_status.get('total_alerts', 0)}")
    print(f"  • Last Alert Time: {system_status.get('last_alert_time', 'Never')}")
    print(f"  • Database Status: {system_status.get('database_status', 'Unknown')}")
    
    if today_summary.get('total_alerts', 0) == 0:
        print(f"\n⚠️ NO SIGNALS TODAY - POTENTIAL CAUSES:")
        print(f"  1. Market Conditions Not Met:")
        print(f"     • SevenSYS requires strong directional movement")
        print(f"     • ATR-based signals need sufficient volatility")
        print(f"     • Current market may be ranging/consolidating")
        print(f"  ")
        print(f"  2. TradingView Chart Issues:")
        print(f"     • Pine script may not be running on active chart")
        print(f"     • Webhook alerts need to be configured in TradingView")
        print(f"     • Chart timeframe affects signal frequency")
        print(f"  ")
        print(f"  3. SevenSYS Pine Script Filters:")
        print(f"     • Signal strength filters (confidence > threshold)")
        print(f"     • ATR volatility requirements")
        print(f"     • Trend confirmation requirements")
        print(f"     • Session time filters (if enabled)")
        
        # Analyze recent market conditions
        analyze_market_conditions_for_sevensys()
    
    else:
        print(f"\n✅ SIGNALS ARE ACTIVE - Recent alerts detected")

def analyze_market_conditions_for_sevensys():
    """Analyze current market conditions that affect SevenSYS signals"""
    print(f"\n📈 MARKET CONDITION ANALYSIS FOR SEVENSYS:")
    
    # Common forex pairs SevenSYS trades
    major_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD']
    
    print(f"  • SevenSYS Signal Requirements:")
    print(f"    - Strong trend direction (EMA alignment)")
    print(f"    - Sufficient ATR volatility for TP/SL calculation")
    print(f"    - Price action confirmation")
    print(f"    - Volume/momentum validation")
    
    print(f"\n  📊 Major Pairs Analysis:")
    for pair in major_pairs:
        print(f"    {pair}:")
        print(f"      - Check TradingView chart for trend strength")
        print(f"      - Verify ATR levels are adequate (>10-20 pips)")
        print(f"      - Confirm SevenSYS indicators are properly aligned")

def check_sevensys_configuration():
    """Check SevenSYS Pine script configuration"""
    print(f"\n⚙️ SEVENSYS CONFIGURATION CHECK:")
    print(f"  1. TradingView Setup:")
    print(f"     • Pine script: 'SevenSYS' should be active on chart")
    print(f"     • Webhook URL: https://jarvis-quant-sys.onrender.com/webhook")
    print(f"     • Alert conditions: Set for both BUY and SELL signals")
    print(f"     • Alert message format: Must include ticker, action, close, SL, TP")
    print(f"  ")
    print(f"  2. Signal Strength Settings:")
    print(f"     • ATR multipliers: Check current settings")
    print(f"     • Trend confirmation: Verify EMA/SMA alignment required")
    print(f"     • Volume filters: May be restricting signals")
    print(f"     • Session filters: May be limiting trading hours")
    print(f"  ")
    print(f"  3. Market Environment:")
    print(f"     • SevenSYS works best in trending markets")
    print(f"     • Sideways/ranging markets = fewer signals")
    print(f"     • Holiday/low volume periods = reduced activity")

def check_webhook_connectivity():
    """Test webhook endpoint connectivity"""
    print(f"\n🔌 WEBHOOK CONNECTIVITY TEST:")
    
    webhook_url = "https://jarvis-quant-sys.onrender.com"
    
    try:
        # Test main endpoint
        response = requests.get(webhook_url, timeout=10)
        if response.status_code == 200:
            print(f"  ✅ Main endpoint: ONLINE")
            data = response.json()
            print(f"     • Service: {data.get('service', 'Unknown')}")
            print(f"     • Environment: {data.get('environment', 'Unknown')}")
            print(f"     • Account: {data.get('account', 'Unknown')}")
        else:
            print(f"  ❌ Main endpoint: ERROR {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Webhook connection failed: {e}")
        print(f"     • Check Render deployment status")
        print(f"     • Verify webhook URL in TradingView alerts")

def provide_troubleshooting_steps():
    """Provide step-by-step troubleshooting"""
    print(f"\n🛠️ TROUBLESHOOTING STEPS:")
    print(f"  1. IMMEDIATE CHECKS:")
    print(f"     ☐ Verify SevenSYS Pine script is active on TradingView chart")
    print(f"     ☐ Check if alerts are configured for BUY/SELL conditions") 
    print(f"     ☐ Confirm webhook URL: https://jarvis-quant-sys.onrender.com/webhook")
    print(f"     ☐ Test webhook connectivity (above)")
    print(f"  ")
    print(f"  2. PINE SCRIPT VERIFICATION:")
    print(f"     ☐ Check SevenSYS.pine file for current signal conditions")
    print(f"     ☐ Verify ATR calculation and threshold settings")
    print(f"     ☐ Check trend detection logic (EMA/SMA alignment)")
    print(f"     ☐ Review signal strength/confidence requirements")
    print(f"  ")
    print(f"  3. MARKET CONDITION ANALYSIS:")
    print(f"     ☐ Check major pairs for trending vs ranging behavior")
    print(f"     ☐ Verify current volatility levels (ATR)")
    print(f"     ☐ Consider time of day/session effects")
    print(f"     ☐ Check for major news events affecting markets")
    print(f"  ")
    print(f"  4. TESTING:")
    print(f"     ☐ Use Memory Dashboard: Run memory_dashboard.py")
    print(f"     ☐ Monitor real-time for next signal")
    print(f"     ☐ Test with manual TradingView alert")

def run_memory_dashboard_info():
    """Show how to run the memory dashboard"""
    print(f"\n📊 SEVENSYS MEMORY DASHBOARD:")
    print(f"  • File: memory_dashboard.py")
    print(f"  • URL: http://127.0.0.1:5001") 
    print(f"  • Features:")
    print(f"    - Real-time webhook monitoring")
    print(f"    - Trade execution tracking")  
    print(f"    - Success/failure analysis")
    print(f"    - Daily performance statistics")
    print(f"  ")
    print(f"  🚀 To start dashboard:")
    print(f"     python memory_dashboard.py")

if __name__ == "__main__":
    analyze_sevensys_conditions()
    check_sevensys_configuration()
    check_webhook_connectivity()
    provide_troubleshooting_steps()
    run_memory_dashboard_info()
    
    print(f"\n" + "=" * 50)
    print(f"🎯 NEXT STEPS:")
    print(f"1. Start Memory Dashboard: python memory_dashboard.py")
    print(f"2. Check TradingView SevenSYS Pine script setup")
    print(f"3. Monitor for signals in current market conditions")
    print(f"4. Verify webhook alerts are properly configured")
    print("=" * 50)
