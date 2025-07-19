import uuid
from journal_logger import log_trade, update_trade_result
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
        
        trade = {
    "id": str(uuid.uuid4()),
    "pair": "BTCUSDT",
    "entry": 45200.0,
    "stop_loss": 44700.0,
    "take_profit": 46000.0,
    "action": "buy",
    "confidence": 0.82,
    "strategy": "MACD+EMA",
    "timestamp": datetime.now().isoformat()
}
log_trade(trade)
        
        return result

    except Exception as e:
        print(f"❌ Error executing trade: {e}")
        return {"status": "error", "message": str(e)}