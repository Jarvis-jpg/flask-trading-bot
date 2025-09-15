#!/usr/bin/env python3
"""
Direct OANDA Account Analysis - Bypass dependency issues
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

def get_oanda_account_data():
    print("🔍 DIRECT OANDA ACCOUNT INVESTIGATION")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # OANDA API credentials
    api_token = os.getenv('OANDA_API_TOKEN')
    account_id = os.getenv('OANDA_ACCOUNT_ID', '001-001-12623605-001')
    environment = os.getenv('OANDA_ENVIRONMENT', 'live')
    
    if environment == 'live':
        api_url = "https://api-fxtrade.oanda.com"
    else:
        api_url = "https://api-fxpractice.oanda.com"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    print(f"📊 Account: {account_id}")
    print(f"🌐 Environment: {environment.upper()}")
    
    try:
        # Get account summary
        print(f"\n💰 ACCOUNT SUMMARY:")
        account_url = f"{api_url}/v3/accounts/{account_id}"
        response = requests.get(account_url, headers=headers)
        
        if response.status_code == 200:
            account_data = response.json()
            account = account_data.get('account', {})
            
            balance = float(account.get('balance', 0))
            nav = float(account.get('NAV', 0))
            unrealized_pl = float(account.get('unrealizedPL', 0))
            margin_used = float(account.get('marginUsed', 0))
            open_trades = int(account.get('openTradeCount', 0))
            
            print(f"   • Balance: ${balance:.2f}")
            print(f"   • NAV: ${nav:.2f}")
            print(f"   • Unrealized P&L: ${unrealized_pl:.2f}")
            print(f"   • Margin Used: ${margin_used:.2f}")
            print(f"   • Open Trades: {open_trades}")
            
            # Calculate daily P&L estimate
            daily_change = balance - 50.0  # Assuming started around $50
            print(f"   • Estimated Daily P&L: ${daily_change:.2f}")
            
        else:
            print(f"   ❌ Error getting account data: {response.status_code}")
            return
        
        # Get recent transactions
        print(f"\n📈 RECENT TRANSACTIONS (Last 50):")
        
        transactions_url = f"{api_url}/v3/accounts/{account_id}/transactions"
        params = {"count": 50, "type": "ORDER_FILL,MARKET_ORDER,TRADE_CLOSE"}
        
        response = requests.get(transactions_url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('transactions', [])
            
            # Filter for today's transactions
            today = datetime.now().date()
            todays_transactions = []
            
            for txn in transactions:
                txn_time_str = txn.get('time', '')
                if txn_time_str:
                    try:
                        txn_time = datetime.fromisoformat(txn_time_str.replace('Z', '+00:00'))
                        if txn_time.date() == today:
                            todays_transactions.append(txn)
                    except:
                        continue
            
            print(f"   Found {len(todays_transactions)} transactions today:")
            
            total_pl = 0.0
            trade_count = 0
            
            for txn in todays_transactions:
                txn_type = txn.get('type', 'Unknown')
                txn_time = txn.get('time', 'Unknown')
                instrument = txn.get('instrument', 'Unknown')
                
                if txn_type == 'MARKET_ORDER':
                    units = txn.get('units', 0)
                    reason = txn.get('reason', 'Unknown')
                    print(f"   📊 {txn_time} | MARKET ORDER: {instrument} {units} units ({reason})")
                    
                elif txn_type == 'ORDER_FILL':
                    units = txn.get('units', 0)
                    price = float(txn.get('price', 0))
                    pl = float(txn.get('pl', 0))
                    total_pl += pl
                    trade_count += 1
                    
                    # Determine if buy or sell
                    side = "BUY" if int(units) > 0 else "SELL"
                    print(f"   💹 {txn_time} | {side}: {instrument} {abs(int(units))} @ {price:.5f} | P&L: ${pl:.2f}")
                    
                elif txn_type == 'TRADE_CLOSE':
                    units = txn.get('units', 0)
                    price = float(txn.get('price', 0))
                    pl = float(txn.get('realizedPL', 0))
                    total_pl += pl
                    
                    side = "CLOSE BUY" if int(units) < 0 else "CLOSE SELL"
                    print(f"   🔚 {txn_time} | {side}: {instrument} {abs(int(units))} @ {price:.5f} | P&L: ${pl:.2f}")
            
            print(f"\n📊 TODAY'S TRADING SUMMARY:")
            print(f"   • Total Trades: {trade_count}")
            print(f"   • Total P&L: ${total_pl:.2f}")
            
            if trade_count > 0:
                print(f"   • Average P&L per trade: ${total_pl/trade_count:.2f}")
                
                if total_pl < 0:
                    print(f"   🚨 SIGNIFICANT LOSSES DETECTED: ${total_pl:.2f}")
                    print(f"   ⚠️  Need to investigate trade logic immediately!")
                
        else:
            print(f"   ❌ Error getting transactions: {response.status_code}")
            
        # Get current open positions
        print(f"\n🎯 CURRENT OPEN POSITIONS:")
        positions_url = f"{api_url}/v3/accounts/{account_id}/positions"
        
        response = requests.get(positions_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            positions = data.get('positions', [])
            
            open_positions = []
            for pos in positions:
                long_units = float(pos.get('long', {}).get('units', 0))
                short_units = float(pos.get('short', {}).get('units', 0))
                
                if long_units != 0 or short_units != 0:
                    open_positions.append(pos)
            
            if open_positions:
                print(f"   Found {len(open_positions)} open positions:")
                for pos in open_positions:
                    instrument = pos.get('instrument', 'Unknown')
                    long_units = float(pos.get('long', {}).get('units', 0))
                    short_units = float(pos.get('short', {}).get('units', 0))
                    long_pl = float(pos.get('long', {}).get('unrealizedPL', 0))
                    short_pl = float(pos.get('short', {}).get('unrealizedPL', 0))
                    
                    if long_units != 0:
                        print(f"   📈 {instrument}: LONG {long_units} units | P&L: ${long_pl:.2f}")
                    if short_units != 0:
                        print(f"   📉 {instrument}: SHORT {abs(short_units)} units | P&L: ${short_pl:.2f}")
            else:
                print("   ℹ️  No open positions")
        
        print(f"\n" + "=" * 60)
        print("🚨 CRITICAL ANALYSIS:")
        
        if len(todays_transactions) > 0:
            print("✅ TRADES DETECTED - The system WAS active today")
            print("🔍 Now need to investigate SevenSYS Pine script logic")
        else:
            print("❌ NO TRADES DETECTED - System may be inactive")
            
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_oanda_account_data()
