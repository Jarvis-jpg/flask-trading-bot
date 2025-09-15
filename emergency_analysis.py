#!/usr/bin/env python3
"""
EMERGENCY TRADING SYSTEM ANALYSIS
Immediate investigation of severe trading losses
"""

from memory_logger import SevenSYSMemoryLogger
import sqlite3
import json
from datetime import datetime, timedelta

def run_emergency_analysis():
    print("🚨 EMERGENCY TRADING SYSTEM ANALYSIS")
    print("=" * 60)
    
    try:
        logger = SevenSYSMemoryLogger()
        
        # Get today's summary
        today = logger.get_today_summary()
        print(f"📊 TODAY ({datetime.now().strftime('%Y-%m-%d')}):")
        print(f"   • Total Alerts: {today.get('total_alerts', 0)}")
        print(f"   • Successful Trades: {today.get('successful_trades', 0)}")
        print(f"   • Failed Trades: {today.get('failed_trades', 0)}")
        print(f"   • Success Rate: {today.get('success_rate', 0):.1f}%")
        
        # Get system status  
        status = logger.get_system_status()
        print(f"\n🖥️ SYSTEM STATUS:")
        print(f"   • Last Alert: {status.get('last_alert_time', 'Never')}")
        print(f"   • Last Execution: {status.get('last_execution_time', 'Never')}")
        print(f"   • Total Historical Trades: {status.get('total_successful_trades', 0)}")
        
        # Get detailed trade analysis
        print(f"\n📢 RECENT ALERTS:")
        for i, alert in enumerate(today.get('recent_alerts', [])[:5]):
            print(f"   {i+1}. {alert.get('timestamp', 'Unknown')} | {alert.get('ticker', '?')} {alert.get('action', '?')} @ {alert.get('price', 0):.5f}")
        
        # Direct database query for more details
        conn = sqlite3.connect(logger.db_path)
        cursor = conn.cursor()
        
        print(f"\n🔍 DETAILED DATABASE ANALYSIS:")
        
        # Check for today's webhook alerts
        cursor.execute('''
            SELECT COUNT(*) FROM webhook_alerts 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        alerts_today = cursor.fetchone()[0]
        print(f"   • Database Webhook Alerts Today: {alerts_today}")
        
        # Check for today's executions
        cursor.execute('''
            SELECT COUNT(*) FROM trade_executions 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        executions_today = cursor.fetchone()[0]
        print(f"   • Database Trade Executions Today: {executions_today}")
        
        # Check for recent failed executions
        cursor.execute('''
            SELECT timestamp, ticker, action, execution_status 
            FROM trade_executions 
            WHERE DATE(timestamp) = DATE('now') AND execution_status LIKE 'FAILED%'
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        failed_trades = cursor.fetchall()
        
        if failed_trades:
            print(f"\n❌ FAILED EXECUTIONS TODAY:")
            for trade in failed_trades:
                print(f"   • {trade[0]} | {trade[1]} {trade[2]} - {trade[3]}")
        
        # Check for successful executions 
        cursor.execute('''
            SELECT timestamp, ticker, action, entry_price, stop_loss, take_profit, oanda_order_id
            FROM trade_executions 
            WHERE DATE(timestamp) = DATE('now') AND execution_status NOT LIKE 'FAILED%'
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        successful_trades = cursor.fetchall()
        
        if successful_trades:
            print(f"\n✅ SUCCESSFUL EXECUTIONS TODAY:")
            for trade in successful_trades:
                print(f"   • {trade[0]} | {trade[1]} {trade[2]} @ {trade[3]:.5f} | SL: {trade[4]:.5f} | TP: {trade[5]:.5f} | Order: {trade[6]}")
        
        conn.close()
        
        # CRITICAL ANALYSIS
        print(f"\n🚨 CRITICAL ISSUES IDENTIFIED:")
        
        if alerts_today == 0:
            print("   ⚠️  NO WEBHOOK ALERTS RECEIVED TODAY")
            print("      - Check TradingView SevenSYS Pine script")
            print("      - Verify webhook alerts are configured")
            print("      - Confirm webhook URL in TradingView")
            
        elif executions_today == 0:
            print("   ⚠️  WEBHOOK ALERTS RECEIVED BUT NO EXECUTIONS")
            print("      - Check OANDA API connection")
            print("      - Verify account balance and margins")
            print("      - Check for API errors in logs")
            
        elif len(failed_trades) > 0:
            print(f"   ⚠️  {len(failed_trades)} FAILED EXECUTIONS DETECTED")
            print("      - Review failure reasons above")
            print("      - Check OANDA API precision issues")
            print("      - Verify TP/SL calculation logic")
            
        # Check if this is actually SevenSYS vs other system
        if alerts_today == 0 and executions_today == 0:
            print(f"\n🤔 POSSIBLE EXPLANATIONS:")
            print("   1. Using different trading system (not SevenSYS)")
            print("   2. Manual trading causing losses (not automated)")
            print("   3. SevenSYS signals not being generated")
            print("   4. Webhook system disconnected")
            
        print(f"\n" + "=" * 60)
        print("🎯 IMMEDIATE ACTIONS REQUIRED:")
        print("1. Check OANDA account for recent trade history")
        print("2. Verify which trading system is actually active")
        print("3. Review TradingView SevenSYS setup and alerts")
        print("4. Check for manual trades vs automated trades")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR in analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_emergency_analysis()
