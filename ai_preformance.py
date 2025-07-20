import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def analyze_performance():
    """Analyze system trading performance"""
    try:
        print("\n📊 System Performance Analysis")
        print("===========================")
        
        # Read trade journal
        with open("logs/trade_journal.json", "r") as f:
            trades = [json.loads(line) for line in f if line.strip()]
        
        df = pd.DataFrame(trades)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Daily performance
        daily_stats = df.groupby(df['timestamp'].dt.date).agg({
            'profit': ['sum', 'mean', 'count'],
            'result': lambda x: (x == 'win').mean() * 100
        }).round(2)
        
        print("\nDaily Performance Summary (Last 5 days):")
        print(daily_stats.tail())
        
        # Plot daily profits
        plt.figure(figsize=(10, 6))
        daily_profits = df.groupby(df['timestamp'].dt.date)['profit'].sum()
        plt.plot(daily_profits.index, daily_profits.values)
        plt.title('Daily Trading Profits')
        plt.xlabel('Date')
        plt.ylabel('Profit ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('logs/daily_performance.png')
        print("\n📈 Daily performance chart saved as 'logs/daily_performance.png'")
        
    except Exception as e:
        print(f"❌ Error analyzing performance: {str(e)}")

if __name__ == "__main__":
    analyze_performance()