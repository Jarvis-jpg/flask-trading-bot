import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def analyze_trades():
    """Analyze trading performance and display statistics"""
    try:
        print("\n📊 Trade Performance Analysis")
        print("===========================")
        
        # Read trade journal
        with open("logs/trade_journal.json", "r") as f:
            trades = [json.loads(line) for line in f if line.strip()]
        
        if not trades:
            print("No trades found to analyze")
            return
            
        df = pd.DataFrame(trades)
        
        # Calculate statistics
        total_trades = len(df)
        win_rate = (df['result'] == 'win').mean() * 100
        total_profit = df['profit'].sum()
        avg_profit = df['profit'].mean()
        
        # Display results
        print(f"\nTotal Trades: {total_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Total Profit: ${total_profit:.2f}")
        print(f"Average Profit per Trade: ${avg_profit:.2f}")
        
        # Show performance by pair
        print("\nPerformance by Pair:")
        pair_stats = df.groupby('pair').agg({
            'result': lambda x: (x == 'win').mean() * 100,
            'profit': ['count', 'sum', 'mean']
        }).round(2)
        
        print(pair_stats)
        
        # Plot performance over time
        plt.figure(figsize=(10, 6))
        df['cumulative_profit'] = df['profit'].cumsum()
        plt.plot(range(len(df)), df['cumulative_profit'])
        plt.title('Cumulative Profit Over Time')
        plt.xlabel('Number of Trades')
        plt.ylabel('Profit ($)')
        plt.savefig('logs/performance.png')
        print("\n📈 Performance chart saved as 'logs/performance.png'")
        
    except Exception as e:
        print(f"❌ Error analyzing trades: {str(e)}")

if __name__ == "__main__":
    analyze_trades()