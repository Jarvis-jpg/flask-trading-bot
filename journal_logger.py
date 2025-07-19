import json
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def ensure_log_directory():
    """Create logs directory if it doesn't exist"""
    try:
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            logging.info(f"Created logs directory at {log_dir}")
        return True
    except Exception as e:
        logging.error(f"Failed to create logs directory: {str(e)}")
        return False

def log_trade(pair, action, entry, stop_loss, take_profit, 
              confidence, strategy, timestamp, result=None, 
              profit=None):
    """
    Log trade details to a JSON file with enhanced error handling
    """
    try:
        # Ensure logs directory exists
        if not ensure_log_directory():
            raise Exception("Could not ensure log directory exists")

        # Prepare log entry
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

        # Get log file path
        log_file = os.path.join(os.getcwd(), 'logs', 'trade_journal.json')
        
        # Write to log file
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            f.flush()  # Ensure write is complete
            
        logging.info(f"Trade logged successfully for {pair}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to log trade: {str(e)}")
        # Print detailed error information
        logging.error(f"Current directory: {os.getcwd()}")
        logging.error(f"Log entry: {log_entry if 'log_entry' in locals() else 'not created'}")
        return False