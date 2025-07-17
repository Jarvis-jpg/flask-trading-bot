from utils.journal_logger import log_trade
from ai_predict import predict_trade_outcome

def execute_trade(trade_data):
    """
    Execute a trade based on the received webhook data
    """
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

        # Get AI prediction
        predicted_result, confidence_score = predict_trade_outcome(trade_data)
        
        # Process trade details
        result = {
            "pair": trade_data["pair"],
            "action": trade_data["action"],
            "entry": float(trade_data["entry"]),
            "stop_loss": float(trade_data["stop_loss"]),
            "take_profit": float(trade_data["take_profit"]),
            "prediction": predicted_result,
            "confidence": confidence_score,
            "status": "executed"
        }
        
        return result

    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        return {"status": "error", "message": str(e)}