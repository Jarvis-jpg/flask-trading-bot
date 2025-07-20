import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def check_ai_accuracy():
    """Analyze AI prediction performance"""
    try:
        print("\n🤖 AI Prediction Analysis")
        print("======================")
        
        # Read trade journal
        with open("logs/trade_journal.json", "r") as f:
            trades = [json.loads(line) for line in f if line.strip()]
        
        df = pd.DataFrame(trades)
        
        # Basic trade statistics
        total_trades = len(df)
        win_rate = (df['result'] == 'win').mean() * 100
        
        print(f"\nTrading Statistics:")
        print(f"Total Trades: {total_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        
        # Performance by pair
        pair_stats = df.groupby('pair').agg({
            'result': lambda x: (x == 'win').mean() * 100,
            'profit': ['count', 'sum', 'mean']
        }).round(2)
        
        print("\nPerformance by Trading Pair:")
        print(pair_stats)
        
        # Plot profit trend
        plt.figure(figsize=(10, 6))
        df['cumulative_profit'] = df['profit'].cumsum()
        plt.plot(range(len(df)), df['cumulative_profit'])
        plt.title('Cumulative Profit Over Time')
        plt.xlabel('Number of Trades')
        plt.ylabel('Profit ($)')
        plt.savefig('logs/trading_performance.png')
        print("\n📈 Performance chart saved as 'logs/trading_performance.png'")
        
    except Exception as e:
        print(f"❌ Error analyzing performance: {str(e)}")

if __name__ == "__main__":
    check_ai_accuracy()