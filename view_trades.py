import json
from datetime import datetime

def view_trades():
    """View all trades in the journal"""
    try:
        print("\n📊 Trade Journal Viewer")
        print("=====================")
        
        with open("logs/trade_journal.json", "r") as f:
            trades = [json.loads(line) for line in f if line.strip()]
            
        if not trades:
            print("No trades found in journal")
            return
            
        print(f"\nFound {len(trades)} trades:")
        for i, trade in enumerate(trades, 1):
            print(f"\nTrade #{i}:")
            print(f"📈 Pair: {trade['pair']}")
            print(f"🎯 Action: {trade['action'].upper()}")
            print(f"💰 Entry: {trade['entry']}")
            print(f"🛑 Stop Loss: {trade['stop_loss']}")
            print(f"🎯 Take Profit: {trade['take_profit']}")
            print(f"📊 Result: {trade['result'].upper()}")
            print(f"💵 Profit: {trade['profit']}")
            print(f"⏰ Time: {trade['timestamp']}")
            print("-" * 40)
            
    except FileNotFoundError:
        print("❌ Trade journal file not found")
    except Exception as e:
        print(f"❌ Error reading trades: {str(e)}")

if __name__ == "__main__":
    view_trades()