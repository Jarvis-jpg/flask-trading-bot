import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_trades():
    """Read trades from journal with error handling"""
    trades = []
    journal_path = Path('logs/trade_journal.json')
    
    if not journal_path.exists():
        logging.error("Trade journal not found")
        return trades
        
    with open(journal_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                if line.strip():
                    # Remove any control characters and normalize whitespace
                    clean_line = ''.join(char for char in line if ord(char) >= 32)
                    trade = json.loads(clean_line)
                    trades.append(trade)
            except json.JSONDecodeError as e:
                logging.warning(f"Invalid JSON at line {line_num}: {e}")
                continue
    
    return trades

def analyze_and_learn():
    """Analyze trading data and train model"""
    print("\n🔍 Reading trade journal...")
    trades = read_trades()
    
    if not trades:
        print("❌ No valid trades found")
        return
        
    print(f"✅ Found {len(trades)} valid trades")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(trades)
    
    # Basic statistics
    print("\n📊 Trade Analysis:")
    print(f"Total trades: {len(df)}")
    if 'result' in df.columns:
        win_rate = (df['result'] == 'win').mean()
        print(f"Win rate: {win_rate:.2%}")

if __name__ == "__main__":
    analyze_and_learn()