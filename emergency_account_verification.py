#!/usr/bin/env python3
"""
EMERGENCY ACCOUNT VERIFICATION
Verify actual OANDA trading activity vs memory logger discrepancy
"""
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.transactions as transactions
from datetime import datetime, timedelta
import json

def verify_account_activity():
    print("🔍 EMERGENCY ACCOUNT VERIFICATION")
    print("=" * 60)
    
    try:
        # OANDA Configuration
        account_id = "001-001-12623605-001"
        access_token = "46ba4cde17b7a48ff25d9a2d6c52b7ca-a5e7c4ffea7b5be5a4e3b1a9ecec4c97"
        
        client = oandapyV20.API(access_token=access_token, environment="live")
        
        print(f"📊 Account ID: {account_id}")
        print(f"🕒 Time: {datetime.now()}")
        
        # Get Account Summary
        print("\n📈 ACCOUNT SUMMARY:")
        print("-" * 40)
        r = accounts.AccountSummary(account_id)
        client.request(r)
        summary = r.response['account']
        
        print(f"Balance: ${float(summary['balance']):,.2f}")
        print(f"NAV: ${float(summary['NAV']):,.2f}")
        print(f"Unrealized P&L: ${float(summary['unrealizedPL']):,.2f}")
        print(f"Margin Used: ${float(summary['marginUsed']):,.2f}")
        print(f"Open Trades: {summary['openTradeCount']}")
        print(f"Open Positions: {summary['openPositionCount']}")
        print(f"Pending Orders: {summary['pendingOrderCount']}")
        
        # Get Today's Transactions
        print("\n📋 TODAY'S TRANSACTIONS:")
        print("-" * 40)
        
        # Get transactions from last 24 hours
        from_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")
        
        params = {
            "from": from_time,
            "type": "ORDER_FILL,MARKET_ORDER,STOP_LOSS_ORDER,TAKE_PROFIT_ORDER"
        }
        
        r = transactions.TransactionList(account_id, params=params)
        client.request(r)
        
        trade_count = 0
        total_pnl = 0.0
        
        transactions_list = r.response.get('transactions', [])
        print(f"Total transactions found: {len(transactions_list)}")
        
        for txn in transactions_list:
            if txn.get('type') == 'ORDER_FILL':
                trade_count += 1
                pnl = float(txn.get('pl', 0))
                total_pnl += pnl
                
                print(f"\n🔹 Trade #{trade_count}:")
                print(f"   Time: {txn.get('time', 'N/A')}")
                print(f"   Instrument: {txn.get('instrument', 'N/A')}")
                print(f"   Units: {txn.get('units', 'N/A')}")
                print(f"   Price: {txn.get('price', 'N/A')}")
                print(f"   P&L: ${pnl:,.2f}")
                print(f"   Reason: {txn.get('reason', 'N/A')}")
        
        print(f"\n📊 TRADING SUMMARY:")
        print(f"   Total Trades Today: {trade_count}")
        print(f"   Total P&L: ${total_pnl:,.2f}")
        
        # Memory Logger Check
        print(f"\n🧠 MEMORY LOGGER COMPARISON:")
        print("-" * 40)
        try:
            from memory_logger import SevenSYSMemoryLogger
            memory_logger = SevenSYSMemoryLogger()
            memory_trades = len(memory_logger.get_trade_history())
            print(f"Memory Logger Records: {memory_trades} trades")
            print(f"OANDA Records: {trade_count} trades")
            print(f"DISCREPANCY: {'YES' if memory_trades != trade_count else 'NO'}")
        except Exception as e:
            print(f"Memory Logger Error: {e}")
        
        return {
            'account_balance': float(summary['balance']),
            'nav': float(summary['NAV']),
            'unrealized_pnl': float(summary['unrealizedPL']),
            'trades_today': trade_count,
            'total_pnl_today': total_pnl,
            'open_trades': int(summary['openTradeCount'])
        }
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    result = verify_account_activity()
    if result:
        print("\n✅ VERIFICATION COMPLETE")
        if result['trades_today'] > 0:
            print("🚨 TRADES DETECTED - Memory logger discrepancy confirmed!")
        else:
            print("ℹ️  No trades found today")
