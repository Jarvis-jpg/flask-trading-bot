from utils.journal_logger import log_trade
from datetime import datetime, UTC
import random

def calculate_realistic_outcome(trade_data):
    """Calculate realistic trade outcome based on market probabilities"""
    try:
        # Realistic win rates based on market conditions
        # Even with a good strategy, 100% win rate is impossible
        # Typical good strategies achieve 40-60% win rate
        win_probability = 0.45  # 45% win rate
        
        # Add randomness but weight it with trade setup quality
        confidence_boost = float(trade_data['confidence']) * 0.1
        final_probability = win_probability + confidence_boost
        
        # Determine outcome
        is_win = random.random() < final_probability
        
        # Calculate profit/loss with realistic risk:reward
        entry = float(trade_data['entry'])
        stop_loss = float(trade_data['stop_loss'])
        take_profit = float(trade_data['take_profit'])
        
        if is_win:
            if trade_data['action'] == 'buy':
                profit = take_profit - entry
            else:
                profit = entry - take_profit
        else:
            if trade_data['action'] == 'buy':
                profit = -(entry - stop_loss)
            else:
                profit = -(stop_loss - entry)
        
        return 'win' if is_win else 'loss', round(profit, 2)
        
    except Exception as e:
        print(f"❌ Error calculating outcome: {e}")
        return 'error', 0.0

def execute_trade(trade_data):
    """Execute a trade with realistic outcomes"""
    try:
        print(f"📈 Processing trade for {trade_data['pair']}")
        
        # Validate required fields
        required_fields = [
            "pair", "action", "entry", "stop_loss", 
            "take_profit", "confidence", "strategy", 
            "timestamp"
        ]
        
        for field in required_fields:
            if field not in trade_data:
                raise ValueError(f"Missing required field: {field}")

        # Calculate realistic outcome
        result, profit = calculate_realistic_outcome(trade_data)
        
        # Prepare trade result
        trade_result = {
            "pair": trade_data["pair"],
            "action": trade_data["action"],
            "entry": float(trade_data["entry"]),
            "stop_loss": float(trade_data["stop_loss"]),
            "take_profit": float(trade_data["take_profit"]),
            "confidence": float(trade_data["confidence"]),
            "strategy": trade_data["strategy"],
            "timestamp": trade_data["timestamp"],
            "result": result,
            "profit": profit,
            "execution_time": datetime.now(UTC).isoformat()
        }
        
        # Log the trade
        log_trade(**trade_result)
        
        print(f"✅ Trade executed: {trade_result['pair']} {trade_result['action']} - {result.upper()}")
        return trade_result

    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        raise