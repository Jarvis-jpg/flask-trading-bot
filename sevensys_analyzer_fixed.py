#!/usr/bin/env python3
"""
SevenSYS Performance Analyzer - Fixed Version
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
    
    def get_recent_transactions(self):
        """Get recent transactions using proper OANDA API"""
        try:
            # Get all transactions (last 500)
            params = {"count": 500}
            r = transactions.TransactionList(accountID=self.account_id, params=params)
            response = self.api.request(r)
            return response.get('transactions', [])
        except Exception as e:
            print(f"? Error getting transactions: {e}")
            return []
    
    def analyze_performance(self):
        """Complete performance analysis"""
        print("?? SEVENSYS PERFORMANCE ANALYSIS (FIXED)")
        print("=" * 60)
        
        # Get account summary
        account = self.get_account_summary()
        if not account:
            return
            
        print(f"?? CURRENT ACCOUNT STATUS:")
        balance = float(account['balance'])
        equity = float(account['NAV'])
        print(f"   Balance: ")
        print(f"   Equity: ")
        print(f"   Unrealized P&L: ")
        print(f"   Open Trades: {account['openTradeCount']}")
        print(f"   Margin Used: ")
        
        # Get recent transactions
        print(f"\n?? RETRIEVING TRADING HISTORY...")
        all_transactions = self.get_recent_transactions()
        
        if not all_transactions:
            print("? No transaction data available")
            return
            
        print(f"   Retrieved {len(all_transactions)} total transactions")
        
        # Filter for order fills (actual trades)
        fills = [t for t in all_transactions if t.get('type') == 'ORDER_FILL']
        
        # Filter for recent fills (last 7 days)
        cutoff_date = datetime.now() - timedelta(days=7)
        recent_fills = []
        
        for fill in fills:
            try:
                trade_time = datetime.fromisoformat(fill.get('time', '').replace('Z', '+00:00'))
                if trade_time >= cutoff_date:
                    recent_fills.append(fill)
            except:
                continue
        
        print(f"   Found {len(recent_fills)} trades in last 7 days")
        
        if not recent_fills:
            print("?? No recent trades found - checking all trades...")
            recent_fills = fills[-20:] if fills else []  # Last 20 trades
        
        if not recent_fills:
            print("? No trade data found")
            return
            
        # Analyze performance
        print(f"\n?? SEVENSYS TRADING PERFORMANCE:")
        wins = 0
        losses = 0
        total_pnl = 0.0
        win_amounts = []
        loss_amounts = []
        
        for fill in recent_fills:
            pnl = float(fill.get('pl', 0))
            total_pnl += pnl
            
            if pnl > 0:
                wins += 1
                win_amounts.append(pnl)
            elif pnl < 0:
                losses += 1
                loss_amounts.append(abs(pnl))
        
        total_trades = len(recent_fills)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        avg_win = sum(win_amounts) / len(win_amounts) if win_amounts else 0
        avg_loss = sum(loss_amounts) / len(loss_amounts) if loss_amounts else 0
        
        print(f"   ?? RESULTS:")
        print(f"      Total Trades: {total_trades}")
        print(f"      Wins: {wins} | Losses: {losses}")
        print(f"      Win Rate: {win_rate:.1f}%")
        print(f"      Total P&L: ")
        print(f"      Average Win: ")
        print(f"      Average Loss: ")
        
        if avg_loss > 0:
            risk_reward = avg_win / avg_loss
            print(f"      Risk/Reward: 1:{risk_reward:.2f}")
        
        # Performance diagnosis
        print(f"\n?? SEVENSYS DIAGNOSIS:")
        
        issues_found = []
        fixes_needed = []
        
        if win_rate < 50:
            issues_found.append(f"? Low win rate ({win_rate:.1f}% - Target: 55%+)")
            fixes_needed.append("• Increase minimum signal strength to 58%")
            fixes_needed.append("• Add stronger trend confirmation")
        
        if total_pnl < 0:
            issues_found.append(f"? Negative P&L ()")
            fixes_needed.append("• URGENT: Reduce position size by 50%")
            fixes_needed.append("• Increase signal threshold to 60%")
            fixes_needed.append("• Enable additional safety filters")
        
        if avg_loss > avg_win * 2:
            issues_found.append("? Losses too large vs wins")
            fixes_needed.append("• Tighten stop losses (reduce ATR multiplier)")
            fixes_needed.append("• Improve take profit targeting")
        
        if len(issues_found) > 0:
            print("   ?? ISSUES IDENTIFIED:")
            for issue in issues_found:
                print(f"      {issue}")
            
            print(f"\n   ?? RECOMMENDED FIXES:")
            for fix in fixes_needed:
                print(f"      {fix}")
        else:
            print("   ? System performing within parameters")
        
        # Show recent trade details
        print(f"\n?? RECENT TRADE HISTORY:")
        for i, fill in enumerate(recent_fills[-10:]):  # Last 10 trades
            instrument = fill.get('instrument', 'Unknown')
            units = fill.get('units', '0')
            price = fill.get('price', '0')
            pnl = float(fill.get('pl', 0))
            time_str = fill.get('time', '').split('T')[0] if 'T' in fill.get('time', '') else 'Unknown'
            
            result = "WIN" if pnl > 0 else "LOSS" if pnl < 0 else "BE"
            emoji = "??" if pnl > 0 else "??" if pnl < 0 else "??"
            
            print(f"   {emoji} {time_str} | {instrument} | {units} units @ {price} | {result} ")
        
        return {
            'account_balance': balance,
            'account_equity': equity,
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'issues_count': len(issues_found),
            'fixes_needed': len(fixes_needed)
        }

if __name__ == "__main__":
    analyzer = SevenSysAnalyzer()
    
    try:
        print("?? Starting SevenSYS Performance Analysis...")
        results = analyzer.analyze_performance()
        
        if results:
            print(f"\n?? Analysis complete!")
            print(f"?? Win Rate: {results['win_rate']:.1f}%")
            print(f"?? Total P&L: ")
            if results['issues_count'] > 0:
                print(f"??  Issues found: {results['issues_count']} - Optimization recommended")
            else:
                print("? System healthy - Continue trading")
        
    except Exception as e:
        print(f"? Analysis failed: {e}")
        import traceback
        traceback.print_exc()
