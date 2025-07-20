# utils
import json
from datetime import datetime
import os
import logging

# Configure logging to console instead of file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_trade(pair, action, entry, stop_loss, take_profit, 
              confidence, strategy, timestamp, result=None, 
              profit=None, execution_time=None):
    """
    Log trade details to a JSON file
    """
    try:
        # Create the trade directory if it doesn't exist
        os.makedirs('trades', exist_ok=True)
        
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
            "execution_time": execution_time or datetime.now().isoformat(),
            "log_time": datetime.now().isoformat()
        }
        
        # Log the entry for debugging
        logging.debug(f"Attempting to log trade: {json.dumps(log_entry)}")
        
        # Write to trade journal
        journal_path = os.path.join('trades', 'trade_journal.json')
        
        # Load existing trades or create new list
        trades = []
        if os.path.exists(journal_path):
            try:
                with open(journal_path, 'r') as f:
                    trades = json.load(f)
            except json.JSONDecodeError:
                trades = []
        
        # Append new trade
        trades.append(log_entry)
        
        # Write all trades back to file
        with open(journal_path, 'w') as f:
            json.dump(trades, f, indent=2)
        
        logging.info(f"Successfully logged trade for {pair}")
        return True
        
    except Exception as e:
        logging.error(f"Error logging trade: {str(e)}")
        logging.error(f"Current working directory: {os.getcwd()}")
        logging.error(f"Attempted to write to: {os.path.join('logs', 'trade_journal.json')}")
        return False