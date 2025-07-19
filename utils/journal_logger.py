# utils
import json
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/debug.log'
)

def log_trade(pair, action, entry, stop_loss, take_profit, 
              confidence, strategy, timestamp, result=None, 
              profit=None):
    """
    Log trade details to a JSON file with debug logging
    """
    try:
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Format the trade data
        log_entry = {
            "pair": pair,
            "action": action,
            "entry": float(entry),
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit),
            "confidence": float(confidence),
            "strategy": strategy,
            "timestamp": timestamp,
            "result": result or "pending",
            "profit": profit or 0.0,
            "log_time": datetime.now().isoformat()
        }
        
        # Log the entry for debugging
        logging.debug(f"Attempting to log trade: {json.dumps(log_entry)}")
        
        # Write to trade journal
        journal_path = os.path.join('logs', 'trade_journal.json')
        with open(journal_path, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
        
        logging.info(f"Successfully logged trade for {pair}")
        return True
        
    except Exception as e:
        logging.error(f"Error logging trade: {str(e)}")
        logging.error(f"Current working directory: {os.getcwd()}")
        logging.error(f"Attempted to write to: {os.path.join('logs', 'trade_journal.json')}")
        return False