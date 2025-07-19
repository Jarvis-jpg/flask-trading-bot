from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome
from datetime import datetime, UTC

def determine_trade_result(trade_data):
    """Determine if trade was win/loss based on entry and current price"""
    try:
        entry = float(trade_data['entry'])
        take_profit = float(trade_data['take_profit'])
        stop_loss = float(trade_data['stop_loss'])
        
        if trade_data['action'] == 'buy':
            if take_profit > entry:
                return 'win', abs(take_profit - entry)
            else:
                return 'loss', abs(stop_loss - entry)
        else:  # sell
            if entry > take_profit:
                return 'win', abs(entry - take_profit)
            else:
                return 'loss', abs(entry - stop_loss)
    except Exception as e:
        print(f"❌ Error determining trade result: {e}")
        return 'unknown', 0.0

def execute_trade(trade_data):
    """Execute a trade based on the received webhook data"""
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

        # Convert numeric values
        trade_data['entry'] = float(trade_data['entry'])
        trade_data['stop_loss'] = float(trade_data['stop_loss'])
        trade_data['take_profit'] = float(trade_data['take_profit'])
        trade_data['confidence'] = float(trade_data['confidence'])

        # Get AI prediction and trade result
        predicted_result, confidence_score = predict_trade_outcome(trade_data)
        trade_result, profit = determine_trade_result(trade_data)
        
        # Log the trade
        log_result = log_trade(
            pair=trade_data["pair"],
            action=trade_data["action"],
            entry=trade_data["entry"],
            stop_loss=trade_data["stop_loss"],
            take_profit=trade_data["take_profit"],
            confidence=trade_data["confidence"],
            strategy=trade_data["strategy"],
            timestamp=trade_data["timestamp"],
            result=trade_result,
            profit=round(profit, 2),
            prediction=predicted_result,
            execution_time=datetime.now(UTC).isoformat()
        )
        
        if not log_result:
            raise Exception("Failed to log trade")

        result = {
            **trade_data,
            "prediction": predicted_result,
            "result": trade_result,
            "profit": round(profit, 2),
            "execution_time": datetime.now(UTC).isoformat()
        }
        
        print(f"✅ Trade executed: {result['pair']} {result['action']} - {result['result'].upper()}")
        return result

    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        raise