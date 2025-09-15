#!/usr/bin/env python3
"""
OANDA Account Investigation - Check actual account activity vs our webhook system
"""

from oanda_client import OandaClient
from datetime import datetime, timedelta
import json

def investigate_oanda_account():
    print("🔍 OANDA ACCOUNT INVESTIGATION")
    print("=" * 60)
    
    try:
        oanda = OandaClient()
        print(f"📊 Account: {oanda.account_id}")
        print(f"🌐 Environment: {oanda.environment}")
        print(f"🔗 API URL: {oanda.api_url}")
        
        # Get account summary
        print(f"\n💰 ACCOUNT SUMMARY:")
        account_info = oanda.get_account_info()
        if isinstance(account_info, dict) and 'account' in account_info:
            account = account_info['account']
            print(f"   • Balance: ${float(account.get('balance', 0)):.2f}")
            print(f"   • NAV: ${float(account.get('NAV', 0)):.2f}")
            print(f"   • Unrealized P&L: ${float(account.get('unrealizedPL', 0)):.2f}")
            print(f"   • Margin Used: ${float(account.get('marginUsed', 0)):.2f}")
            print(f"   • Open Trades: {account.get('openTradeCount', 0)}")
            print(f"   • Open Positions: {account.get('openPositionCount', 0)}")
        else:
            print(f"   ❌ Error getting account info: {account_info}")
        
        # Get recent transactions
        print(f"\n📈 RECENT TRANSACTIONS (Last 24 hours):")
        
        # Try to get transactions
        try:
            import requests
            
            # Calculate time range for last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            # Format for OANDA API
            from_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
            to_time = end_time.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
            
            url = f"{oanda.api_url}/v3/accounts/{oanda.account_id}/transactions"
            headers = {
                "Authorization": f"Bearer {oanda.api_token}",
                "Content-Type": "application/json"
            }
            params = {
                "from": from_time,
                "to": to_time,
                "pageSize": 50
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('transactions', [])
                
                if transactions:
                    print(f"   Found {len(transactions)} transactions:")
                    
                    trade_transactions = []
                    order_transactions = []
                    
                    for txn in transactions[-10:]:  # Last 10 transactions
                        txn_type = txn.get('type', 'Unknown')
                        txn_time = txn.get('time', 'Unknown')
                        
                        if txn_type in ['MARKET_ORDER', 'ORDER_FILL', 'TRADE_CLOSE']:
                            if txn_type == 'MARKET_ORDER':
                                instrument = txn.get('instrument', 'Unknown')
                                units = txn.get('units', 0)
                                reason = txn.get('reason', 'Unknown')
                                print(f"   📊 {txn_time} | MARKET ORDER: {instrument} {units} units ({reason})")
                                order_transactions.append(txn)
                                
                            elif txn_type == 'ORDER_FILL':
                                instrument = txn.get('instrument', 'Unknown')
                                units = txn.get('units', 0)
                                price = txn.get('price', 0)
                                pl = txn.get('pl', 0)
                                print(f"   💹 {txn_time} | ORDER FILL: {instrument} {units} @ {price} | P&L: ${pl}")
                                trade_transactions.append(txn)
                                
                            elif txn_type == 'TRADE_CLOSE':
                                instrument = txn.get('instrument', 'Unknown')
                                units = txn.get('units', 0)
                                price = txn.get('price', 0)
                                pl = txn.get('realizedPL', 0)
                                print(f"   🔚 {txn_time} | TRADE CLOSE: {instrument} {units} @ {price} | P&L: ${pl}")
                                trade_transactions.append(txn)
                    
                    # Analyze if trades match our webhook system
                    print(f"\n🔍 TRADE SOURCE ANALYSIS:")
                    webhook_originated = 0
                    manual_or_other = len(trade_transactions)
                    
                    for txn in order_transactions:
                        reason = txn.get('reason', '')
                        client_extensions = txn.get('clientExtensions', {})
                        comment = client_extensions.get('comment', '')
                        
                        if 'webhook' in reason.lower() or 'jarvis' in comment.lower() or 'sevensys' in comment.lower():
                            webhook_originated += 1
                            manual_or_other -= 1
                    
                    print(f"   • Webhook/Automated Trades: {webhook_originated}")
                    print(f"   • Manual/Other Trades: {manual_or_other}")
                    
                    if manual_or_other > 0 and webhook_originated == 0:
                        print(f"\n🚨 CRITICAL FINDING:")
                        print(f"   ⚠️  ALL RECENT TRADES APPEAR TO BE MANUAL OR FROM DIFFERENT SYSTEM")
                        print(f"   ⚠️  NO WEBHOOK/SEVENSYS TRADES DETECTED")
                        print(f"   ⚠️  THE LOSSES ARE NOT FROM OUR AUTOMATED SYSTEM")
                        
                else:
                    print("   ℹ️  No transactions found in last 24 hours")
                    
            else:
                print(f"   ❌ Error getting transactions: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error querying transactions: {e}")
        
        # Get current open positions
        print(f"\n🎯 CURRENT OPEN POSITIONS:")
        try:
            url = f"{oanda.api_url}/v3/accounts/{oanda.account_id}/positions"
            headers = {"Authorization": f"Bearer {oanda.api_token}"}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                positions = data.get('positions', [])
                
                open_positions = [pos for pos in positions if float(pos.get('long', {}).get('units', 0)) != 0 or float(pos.get('short', {}).get('units', 0)) != 0]
                
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
            else:
                print(f"   ❌ Error getting positions: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error querying positions: {e}")
        
        print(f"\n" + "=" * 60)
        print("🎯 CONCLUSIONS:")
        print("1. Check if trades were made manually or via different system")
        print("2. Our SevenSYS webhook system shows NO activity today")
        print("3. Any losses are NOT from our automated trading system")
        print("4. Investigate other trading platforms or manual trading")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR in OANDA investigation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_oanda_account()
