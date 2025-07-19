from utils.journal_logger import log_trade
from datetime import datetime

def test_logging():
    """Test the logging functionality"""
    print("\n🔍 Testing trade logging...")
    
    try:
        test_trade = {
            "pair": "BTCUSDT",
            "action": "buy",
            "entry": 45000.00,
            "stop_loss": 44500.00,
            "take_profit": 46000.00,
            "confidence": 0.75,
            "strategy": "TEST",
            "timestamp": datetime.now().isoformat(),
            "result": "win",
            "profit": 100.00
        }
        
        success = log_trade(**test_trade)
        
        if success:
            print("✅ Test trade logged successfully")
            # Verify the log file
            with open('logs/trade_journal.json', 'r') as f:
                last_line = f.readlines()[-1]
                print(f"\nLast logged trade:\n{last_line}")
        else:
            print("❌ Failed to log test trade")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_logging()