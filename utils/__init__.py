import json
from datetime import datetime
import os
import logging

def log_trade(pair, action, entry, stop_loss, take_profit, 
              confidence, strategy, timestamp, result=None, 
              profit=None):
    """Log trade details to a JSON file"""
    try:
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Prepare log entry
        log_entry = {
            "pair": str(pair),
            "action": str(action),
            "entry": float(entry),
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit),
            "confidence": float(confidence),
            "strategy": str(strategy),
            "timestamp": str(timestamp),
            "result": str(result) if result else "pending",
            "profit": float(profit) if profit else 0.0,
            "log_time": datetime.now().isoformat()
        }

        # Write to trade journal
        journal_path = os.path.join(os.getcwd(), 'logs', 'trade_journal.json')
        with open(journal_path, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        print(f"✅ Trade logged for {pair}")
        return True
        
    except Exception as e:
        print(f"❌ Error logging trade: {str(e)}")
        print(f"Current directory: {os.getcwd()}")
        return False