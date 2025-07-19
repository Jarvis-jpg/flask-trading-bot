from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome
from datetime import datetime, UTC
import logging

def execute_trade(trade_data):
    """Execute a trade based on the received webhook data"""
    try:
        logging.info(f"Processing trade for {trade_data['pair']}")
        
        # Validate required fields
        required_fields = [
            "pair", "action", "entry", "stop_loss", 
            "take_profit", "confidence", "strategy", 
            "timestamp"
        ]
        
        for field in required_fields:
            if field not in trade_data:
                raise ValueError(f"Missing required field: {field}")

        # Convert numeric values
        entry = float(trade_data['entry'])
        stop_loss = float(trade_data['stop_loss'])
        take_profit = float(trade_data['take_profit'])
        
        # Calculate result
        if trade_data['action'] == 'buy':
            result = 'win' if take_profit > entry else 'loss'
            profit = take_profit - entry if result == 'win' else entry - stop_loss
        else:
            result = 'win' if entry > take_profit else 'loss'
            profit = entry - take_profit if result == 'win' else stop_loss - entry

        # Log the trade
        log_success = log_trade(
            pair=trade_data["pair"],
            action=trade_data["action"],
            entry=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            confidence=trade_data["confidence"],
            strategy=trade_data["strategy"],
            timestamp=trade_data["timestamp"],
            result=result,
            profit=round(abs(profit), 2)
        )

        if not log_success:
            raise Exception("Failed to log trade - check logs for details")

        # Return trade result
        return {
            **trade_data,
            "result": result,
            "profit": round(abs(profit), 2),
            "log_time": datetime.now(UTC).isoformat()
        }

    except Exception as e:
        logging.error(f"Error executing trade: {str(e)}")
        raise