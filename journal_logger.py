import json
from datetime import datetime
import os

def log_trade(pair=None, action=None, entry=None, stop_loss=None, 
              take_profit=None, confidence=None, strategy=None, 
              timestamp=None, result=None, profit=None, prediction=None, 
              execution_time=None):
    """
    Log trade details to a JSON file with all necessary fields
    """
    try:
        log_entry = {
            "pair": pair,
            "action": action,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence,
            "strategy": strategy,
            "timestamp": timestamp,
            "result": result,
            "profit": profit,
            "prediction": prediction,
            "execution_time": execution_time or datetime.now().isoformat()
        }

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Append to trade log file
        with open('logs/trade_journal.json', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        print(f"📝 Trade logged successfully for {pair}")
        return True
        
    except Exception as e:
        print(f"❌ Error logging trade: {e}")
        return False