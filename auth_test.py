#!/usr/bin/env python3
"""
Test OANDA Authentication and Get Real Account Data
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

def test_oanda_auth():
    print("🔐 TESTING OANDA AUTHENTICATION")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('OANDA_API_KEY')
    account_id = os.getenv('OANDA_ACCOUNT_ID')
    
    print(f"📋 API Key: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else api_key}")
    print(f"📋 Account ID: {account_id}")
    
    # Determine environment
    if account_id and account_id.startswith('001-001-'):
        environment = "live"
        api_url = "https://api-fxtrade.oanda.com"
    else:
        environment = "practice"
        api_url = "https://api-fxpractice.oanda.com"
    
    print(f"🌐 Environment: {environment.upper()}")
    print(f"🔗 API URL: {api_url}")
    
    # Test authentication
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n💰 TESTING ACCOUNT ACCESS:")
    
    try:
        # Test account summary
        url = f"{api_url}/v3/accounts/{account_id}"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📡 Response Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            account = data.get('account', {})
            
            print(f"✅ Authentication: SUCCESS")
            print(f"💵 Balance: ${float(account.get('balance', 0)):.2f}")
            print(f"📊 NAV: ${float(account.get('NAV', 0)):.2f}")  
            print(f"📈 Unrealized P&L: ${float(account.get('unrealizedPL', 0)):.2f}")
            print(f"🏦 Margin Used: ${float(account.get('marginUsed', 0)):.2f}")
            print(f"📋 Open Trades: {account.get('openTradeCount', 0)}")
            print(f"🎯 Open Positions: {account.get('openPositionCount', 0)}")
            
        elif response.status_code == 401:
            print(f"❌ Authentication: FAILED")
            print(f"🔐 Error: Invalid API key or account ID")
            print(f"📝 Response: {response.text}")
            return False
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False
    
    print(f"\n📈 GETTING TRANSACTION HISTORY:")
    
    try:
        # Get transactions from last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        
        from_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
        to_time = end_time.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
        
        url = f"{api_url}/v3/accounts/{account_id}/transactions"
        params = {
            'from': from_time,
            'to': to_time,
            'pageSize': 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            transactions = data.get('transactions', [])
            
            print(f"📊 Found {len(transactions)} transactions in last 24 hours")
            
            if transactions:
                print(f"\n🔍 RECENT TRADING ACTIVITY:")
                
                trade_count = 0
                total_pnl = 0.0
                
                for txn in transactions:
                    txn_type = txn.get('type', 'Unknown')
                    txn_time = txn.get('time', 'Unknown')
                    
                    if txn_type in ['MARKET_ORDER', 'ORDER_FILL', 'TRADE_CLOSE']:
                        trade_count += 1
                        
                        if txn_type == 'MARKET_ORDER':
                            instrument = txn.get('instrument', 'Unknown')
                            units = txn.get('units', 0)
                            reason = txn.get('reason', 'Unknown')
                            print(f"   📊 {txn_time} | MARKET ORDER: {instrument} {units} units ({reason})")
                            
                        elif txn_type == 'ORDER_FILL':
                            instrument = txn.get('instrument', 'Unknown')
                            units = txn.get('units', 0)
                            price = txn.get('price', 0)
                            pl = float(txn.get('pl', 0))
                            total_pnl += pl
                            print(f"   💹 {txn_time} | ORDER FILL: {instrument} {units} @ {price} | P&L: ${pl:.2f}")
                            
                        elif txn_type == 'TRADE_CLOSE':
                            instrument = txn.get('instrument', 'Unknown')
                            units = txn.get('units', 0)
                            price = txn.get('price', 0)
                            pl = float(txn.get('realizedPL', 0))
                            total_pnl += pl
                            print(f"   🔚 {txn_time} | TRADE CLOSE: {instrument} {units} @ {price} | P&L: ${pl:.2f}")
                
                print(f"\n📊 TRADING SUMMARY:")
                print(f"   • Total Trade Transactions: {trade_count}")
                print(f"   • Total P&L Today: ${total_pnl:.2f}")
                
                if trade_count > 0:
                    print(f"\n🚨 CONFIRMATION: TRADES WERE EXECUTED TODAY")
                    print(f"   The system DID generate {trade_count} trading transactions")
                    
            else:
                print(f"   ℹ️  No transactions found in last 24 hours")
                
        else:
            print(f"❌ Error getting transactions: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error querying transactions: {e}")
    
    return True

if __name__ == "__main__":
    test_oanda_auth()
