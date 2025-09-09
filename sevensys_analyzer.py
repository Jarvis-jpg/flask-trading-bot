#!/usr/bin/env python3
"""
SevenSYS Performance Analyzer
Automatically connects to OANDA API and analyzes recent trading performance
"""

import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.transactions as transactions
from datetime import datetime, timedelta
import json
from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID

class SevenSysAnalyzer:
    def __init__(self):
        self.api = oandapyV20.API(access_token=OANDA_API_KEY, environment="live")
        self.account_id = OANDA_ACCOUNT_ID
        
    def get_account_summary(self):
        """Get current account status"""
        try:
            r = accounts.AccountSummary(accountID=self.account_id)
            response = self.api.request(r)
            return response['account']
        except Exception as e:
            print(f"? Error getting account summary: {e}")
            return None
    
    def get_recent_transactions(self, days=7):
        """Get recent transactions for analysis"""
        try:
            # Get transactions from last N days
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S.000000000Z')
            
            params = {
                "from": from_date,
                "type": ["ORDER_FILL"]
            }
            
            r = transactions.TransactionsSinceID(accountID=self.account_id, params=params)
            response = self.api.request(r)
            return response.get('transactions', [])
        except Exception as e:
            print(f"? Error getting transactions: {e}")
            return []
    
    def analyze_performance(self):
        """Complete performance analysis"""
        print("?? SEVENSYS PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        # Get account summary
        account = self.get_account_summary()
        if not account:
            return
            
        print(f"?? ACCOUNT STATUS:")
        print(f"   Balance: USD {float(account['balance']):,.2f}")
        print(f"   Equity: USD {float(account['NAV']):,.2f}")
        print(f"   Open Trades: {account['openTradeCount']}")
        
        # Get recent transactions
        print(f"\n?? ANALYZING RECENT TRADING ACTIVITY...")
        transactions_data = self.get_recent_transactions(days=7)
        
        if not transactions_data:
            print("? No recent transactions found")
            return
            
        # Filter and analyze trades
        fills = [t for t in transactions_data if t.get('type') == 'ORDER_FILL']
        
        if not fills:
            print("? No order fills found in recent data")
            return
            
        print(f"\n?? TRADE ANALYSIS (Last 7 Days):")
        print(f"   Total Trades: {len(fills)}")
        
        wins = 0
        losses = 0
        total_pnl = 0
        
        for fill in fills:
            pnl = float(fill.get('pl', 0))
            total_pnl += pnl
            
            if pnl > 0:
                wins += 1
            elif pnl < 0:
                losses += 1
                
        win_rate = (wins / len(fills)) * 100 if fills else 0
        
        print(f"   Wins: {wins} | Losses: {losses}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Total P&L: USD {total_pnl:.2f}")
        
        # Analysis and recommendations
        print(f"\n?? PERFORMANCE ANALYSIS:")
        
        if win_rate < 50:
            print(f"   ??  ISSUE: Low win rate ({win_rate:.1f}%)")
            print(f"   ?? FIXES: Increase signal strength to 55%+")
        
        if total_pnl < 0:
            print(f"   ?? CRITICAL: Negative P&L - System needs immediate optimization")
        else:
            print(f"   ? Positive P&L - System performing")
        
        # Recent trades detail
        print(f"\n?? LAST 10 TRADES:")
        for fill in fills[-10:]:
            instrument = fill.get('instrument', 'Unknown')
            pnl = float(fill.get('pl', 0))
            time_str = fill.get('time', '').split('T')[0] if 'T' in fill.get('time', '') else 'Unknown'
            
            status = "WIN" if pnl > 0 else "LOSS"
            emoji = "??" if pnl > 0 else "??"
            
            print(f"   {emoji} {time_str} | {instrument} | {status} USD {pnl:.2f}")
            
        return {
            'total_trades': len(fills),
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl
        }

if __name__ == "__main__":
    analyzer = SevenSysAnalyzer()
    
    try:
        results = analyzer.analyze_performance()
        print(f"\n?? ANALYSIS COMPLETE!")
        
    except Exception as e:
        print(f"? Analysis failed: {e}")
