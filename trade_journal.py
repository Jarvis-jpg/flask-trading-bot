import json
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_trade_journal():
    """Read trade journal line by line to handle potential JSON errors"""
    trades = []
    journal_path = Path('logs/trade_journal.json')
    
    if not journal_path.exists():
        logging.error("❌ Trade journal file not found")
        return []
    
    with open(journal_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                if line.strip():  # Skip empty lines
                    trade = json.loads(line.strip())
                    trades.append(trade)
            except json.JSONDecodeError as e:
                logging.warning(f"⚠️ Invalid JSON at line {line_num}: {str(e)}")
                continue
    
    return trades

def analyze_and_learn():
    """Analyze trade data and update AI model"""
    print("📊 Training AI model from trade_journal.json...")
    
    try:
        # Read trades
        trades = read_trade_journal()
        if not trades:
            print("❌ No valid trades found for analysis")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(trades)
        
        # Basic statistics
        total_trades = len(df)
        win_rate = (df['result'] == 'win').mean() if 'result' in df.columns else 0
        
        print(f"\n📈 Trade Analysis:")
        print(f"Total trades analyzed: {total_trades}")
        print(f"Win rate: {win_rate:.2%}")
        
        # TODO: Add your AI model training code here
        
    except Exception as e:
        logging.error(f"❌ Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        analyze_and_learn()
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")