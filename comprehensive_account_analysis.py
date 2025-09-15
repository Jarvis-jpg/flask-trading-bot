#!/usr/bin/env python3
"""
COMPREHENSIVE OANDA ACCOUNT ANALYSIS
Check all trades, balance changes, and webhook activity for today
"""

from oanda_client import OandaClient
from memory_logger import SevenSYSMemoryLogger
import requests
import json
from datetime import datetime, timedelta
import sqlite3

def analyze_account_comprehensive():
    print("🔍 COMPREHENSIVE OANDA ACCOUNT ANALYSIS")
    print("=" * 70)
    
    try:
        oanda = OandaClient()
        
        # Get current account summary
        print(f"📊 ACCOUNT SUMMARY:")
        account_info = oanda.get_account_info()
        
        if isinstance(account_info, dict) and 'account' in account_info:
            account = account_info['account']
            current_balance = float(account.get('balance', 0))
            current_nav = float(account.get('NAV', 0))
            unrealized_pl = float(account.get('unrealizedPL', 0))
            margin_used = float(account.get('marginUsed', 0))
            open_trades = int(account.get('openTradeCount', 0))
            
            print(f"   • Current Balance: ${current_balance:.2f}")
            print(f"   • NAV: ${current_nav:.2f}")
            print(f"   • Unrealized P&L: ${unrealized_pl:.2f}")
            print(f"   • Margin Used: ${margin_used:.2f}")
            print(f"   • Open Trades: {open_trades}")
            
        else:
            print(f"   ❌ Error getting account info: {account_info}")
            return
        
        # Get detailed transactions for today
        print(f"\n📈 DETAILED TRANSACTIONS - TODAY ({datetime.now().strftime('%Y-%m-%d')}):")
        
        # Calculate today's time range
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        from_time = today_start.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
        to_time = today_end.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
        
        url = f"{oanda.api_url}/v3/accounts/{oanda.account_id}/transactions"
        headers = {"Authorization": f"Bearer {oanda.api_token}", "Content-Type": "application/json"}
        params = {"from": from_time, "to": to_time, "pageSize": 100}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('transactions', [])
            
            print(f"   Found {len(transactions)} total transactions today")
            
            # Categorize transactions
            market_orders = []
            order_fills = []
            trade_closes = []
            stop_loss_orders = []
            take_profit_orders = []
            
            total_realized_pl = 0.0
            
            for txn in transactions:
                txn_type = txn.get('type', '')
                
                if txn_type == 'MARKET_ORDER':
                    market_orders.append(txn)
                elif txn_type == 'ORDER_FILL':
                    order_fills.append(txn)
                    pl = float(txn.get('pl', 0))
                    total_realized_pl += pl
                elif txn_type == 'TRADE_CLOSE':
                    trade_closes.append(txn)
                    pl = float(txn.get('realizedPL', 0))
                    total_realized_pl += pl
                elif txn_type == 'STOP_LOSS_ORDER':
                    stop_loss_orders.append(txn)
                elif txn_type == 'TAKE_PROFIT_ORDER':
                    take_profit_orders.append(txn)
            
            print(f"\n   📊 TRANSACTION BREAKDOWN:")
            print(f"   • Market Orders: {len(market_orders)}")
            print(f"   • Order Fills: {len(order_fills)}")
            print(f"   • Trade Closes: {len(trade_closes)}")
            print(f"   • Stop Loss Orders: {len(stop_loss_orders)}")
            print(f"   • Take Profit Orders: {len(take_profit_orders)}")
            print(f"   • Total Realized P&L Today: ${total_realized_pl:.2f}")
            
            # Detailed analysis of market orders (entry signals)
            if market_orders:
                print(f"\n   🎯 MARKET ORDERS ANALYSIS (Entry Signals):")
                for i, order in enumerate(market_orders, 1):
                    time = order.get('time', 'Unknown')
                    instrument = order.get('instrument', 'Unknown')
                    units = order.get('units', '0')
                    reason = order.get('reason', 'Unknown')
                    
                    # Determine if buy or sell
                    units_float = float(units)
                    direction = "BUY" if units_float > 0 else "SELL"
                    
                    print(f"      {i}. {time} | {instrument} {direction} {abs(units_float)} units")
                    print(f"         Reason: {reason}")
            
            # Detailed analysis of order fills and their P&L
            if order_fills:
                print(f"\n   💹 ORDER FILLS ANALYSIS (Executions & Exits):")
                for i, fill in enumerate(order_fills, 1):
                    time = fill.get('time', 'Unknown')
                    instrument = fill.get('instrument', 'Unknown')
                    units = fill.get('units', '0')
                    price = float(fill.get('price', 0))
                    pl = float(fill.get('pl', 0))
                    reason = fill.get('reason', 'Unknown')
                    
                    units_float = float(units)
                    direction = "BUY" if units_float > 0 else "SELL"
                    
                    pl_color = "PROFIT" if pl > 0 else "LOSS" if pl < 0 else "BREAKEVEN"
                    
                    print(f"      {i}. {time} | {instrument} {direction} {abs(units_float)} @ {price:.5f}")
                    print(f"         P&L: ${pl:.2f} ({pl_color}) | Reason: {reason}")
            
            # Check if stop losses were hit
            stop_loss_hits = [fill for fill in order_fills if 'STOP_LOSS' in fill.get('reason', '')]
            if stop_loss_hits:
                print(f"\n   🛑 STOP LOSS HITS ({len(stop_loss_hits)} trades):")
                total_sl_loss = 0
                for hit in stop_loss_hits:
                    time = hit.get('time', 'Unknown')
                    instrument = hit.get('instrument', 'Unknown')
                    pl = float(hit.get('pl', 0))
                    price = float(hit.get('price', 0))
                    total_sl_loss += pl
                    
                    print(f"      • {time} | {instrument} @ {price:.5f} | Loss: ${pl:.2f}")
                
                print(f"      💸 Total Stop Loss Losses: ${total_sl_loss:.2f}")
        
        # Check webhook database for comparison
        print(f"\n🔍 WEBHOOK DATABASE COMPARISON:")
        try:
            memory_logger = SevenSYSMemoryLogger()
            
            conn = sqlite3.connect(memory_logger.db_path)
            cursor = conn.cursor()
            
            # Get today's webhooks
            cursor.execute('''
                SELECT COUNT(*) FROM webhook_alerts 
                WHERE DATE(timestamp) = DATE('now')
            ''')
            webhook_alerts_today = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM trade_executions 
                WHERE DATE(timestamp) = DATE('now')
            ''')
            webhook_executions_today = cursor.fetchone()[0]
            
            print(f"   • Webhook Alerts Logged: {webhook_alerts_today}")
            print(f"   • Webhook Executions Logged: {webhook_executions_today}")
            print(f"   • OANDA Market Orders: {len(market_orders) if 'market_orders' in locals() else 0}")
            
            # If there's a discrepancy, investigate
            if len(market_orders) > webhook_executions_today:
                print(f"\n   ⚠️  DISCREPANCY DETECTED!")
                print(f"   • OANDA shows {len(market_orders)} market orders")
                print(f"   • Webhook system logged {webhook_executions_today} executions")
                print(f"   • Missing {len(market_orders) - webhook_executions_today} webhook logs")
                print(f"   • This suggests trades came from different source!")
            
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Error checking webhook database: {e}")
        
        print(f"\n" + "=" * 70)
        print(f"🚨 ANALYSIS CONCLUSIONS:")
        
        if 'total_realized_pl' in locals() and total_realized_pl < -10:
            print(f"   💸 SIGNIFICANT LOSSES DETECTED: ${total_realized_pl:.2f}")
        
        if 'stop_loss_hits' in locals() and len(stop_loss_hits) > 0:
            print(f"   🛑 {len(stop_loss_hits)} STOP LOSSES HIT TODAY")
        
        if len(market_orders) > 0:
            print(f"   📈 {len(market_orders)} TRADES EXECUTED TODAY")
            print(f"   🤔 NEED TO VERIFY SOURCE OF THESE TRADES")
        
        print(f"=" * 70)
        
    except Exception as e:
        print(f"❌ ERROR in comprehensive analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_account_comprehensive()
