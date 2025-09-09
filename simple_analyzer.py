import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.transactions as transactions
from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID
import json

def analyze_sevensys():
    try:
        api = oandapyV20.API(access_token=OANDA_API_KEY, environment="live")
        
        print("SEVENSYS PERFORMANCE ANALYSIS")
        print("=" * 50)
        
        # Get account info
        r = accounts.AccountSummary(accountID=OANDA_ACCOUNT_ID)
        account_data = api.request(r)
        account = account_data['account']
        
        balance = float(account['balance'])
        equity = float(account['NAV'])
        
        print(f"Account Balance: ${balance:.2f}")
        print(f"Account Equity: ${equity:.2f}")
        print(f"Unrealized P&L: ${equity - balance:.2f}")
        print(f"Open Trades: {account['openTradeCount']}")
        
        # Get transactions
        params = {'count': 500}
        r = transactions.TransactionList(accountID=OANDA_ACCOUNT_ID, params=params)
        trans_data = api.request(r)
        all_transactions = trans_data.get('transactions', [])
        
        # Filter for order fills
        fills = []
        for t in all_transactions:
            if t.get('type') == 'ORDER_FILL':
                fills.append(t)
        
        print(f"\nFound {len(fills)} completed trades")
        
        if len(fills) == 0:
            print("No trade data found")
            return
        
        # Analyze trades
        wins = 0
        losses = 0
        total_pnl = 0.0
        
        for fill in fills:
            pnl = float(fill.get('pl', 0))
            total_pnl += pnl
            if pnl > 0:
                wins += 1
            elif pnl < 0:
                losses += 1
        
        total_trades = len(fills)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        print(f"\nTRADING RESULTS:")
        print(f"Total Trades: {total_trades}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total P&L: ${total_pnl:.2f}")
        
        # Show recent trades
        print(f"\nLAST 15 TRADES:")
        recent_fills = fills[-15:] if len(fills) >= 15 else fills
        
        for fill in recent_fills:
            instrument = fill.get('instrument', 'N/A')
            pnl = float(fill.get('pl', 0))
            time_str = fill.get('time', 'N/A')
            if 'T' in time_str:
                time_str = time_str.split('T')[0]
            
            result = "WIN" if pnl > 0 else "LOSS" if pnl < 0 else "BE"
            print(f"  {time_str} | {instrument} | {result} ${pnl:.2f}")
        
        # Analysis
        print(f"\nANALYSIS:")
        starting_balance = 50.0
        current_return = ((balance - starting_balance) / starting_balance) * 100
        print(f"Starting Balance: ${starting_balance:.2f}")
        print(f"Current Return: {current_return:.1f}%")
        
        if win_rate < 50:
            print("ISSUE: Win rate below 50% - need better signals")
        if total_pnl < 0:
            print("ISSUE: Negative P&L - system underperforming")
        if current_return > -20:
            print("STATUS: Acceptable drawdown - system recoverable")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Check OANDA connection and credentials")

if __name__ == "__main__":
    analyze_sevensys()
