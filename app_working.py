import logging
import json
from flask import Flask, request, jsonify
from oanda_client import OandaClient
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Flask app
app = Flask(__name__)

# Initialize OANDA client
oanda = OandaClient()

def calculate_position_size(price, stop_loss, account_balance=25000, risk_percent=4.0):
    try:
        risk_amount = account_balance * (risk_percent / 100)
        price_difference = abs(float(price) - float(stop_loss))
        if price_difference == 0:
            return 500  # Conservative default for small account
        position_size = round(risk_amount / price_difference)
        return max(1, min(position_size, 1000))  # Cap at 1000 for small account
    except Exception as e:
        logging.error(f"Error calculating position size: {e}")
        return 500

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "JARVIS Trading System",
        "environment": oanda.environment,
        "account": oanda.account_id
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        logging.info(f"Received webhook data: {json.dumps(data, indent=2)}")

        # Extract data from TradingView webhook format
        symbol = data.get("ticker") or data.get("symbol", "")
        action = data.get("strategy.order.action") or data.get("action", "")
        price = data.get("close") or data.get("price", 0)
        stop_loss = data.get("stop_loss", 0)
        take_profit = data.get("take_profit", 0)
        
        if not all([symbol, action, price, stop_loss, take_profit]):
            missing = [k for k, v in {"symbol": symbol, "action": action, "price": price, "stop_loss": stop_loss, "take_profit": take_profit}.items() if not v]
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        # Calculate position size (conservative for small account)
        position_size = calculate_position_size(price, stop_loss, account_balance=45.0, risk_percent=2.0)
        units = position_size if action.lower() == "buy" else -position_size
        
        trade_data = {
            "symbol": symbol,
            "units": units,
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit)
        }

        logging.info(f"Placing trade: {action} {abs(units)} units of {symbol}")
        
        trade_result = oanda.place_trade(trade_data)
        
        if isinstance(trade_result, dict) and "error" not in trade_result:
            logging.info("Trade placed successfully")
            return jsonify({
                "status": "success", 
                "message": "Trade placed successfully",
                "trade_data": trade_result
            }), 200
        else:
            error_msg = trade_result.get("error", "Unknown error") if isinstance(trade_result, dict) else "Invalid response"
            logging.error(f"Trade failed: {error_msg}")
            return jsonify({"status": "error", "message": error_msg}), 500
            
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("\nOANDA Configuration:")
    print(f"  - Account: {oanda.account_id}")
    print(f"  - Mode: {oanda.environment.upper()}")
    print(f"  - API URL: {oanda.api_url}")
    
    print("\nStarting Jarvis Trading Bot...")
    print("Routes configured:")
    print("  - GET  /")
    print("  - POST /webhook")
    
    print("\nConfiguration:")
    print("  - Host: 0.0.0.0")
    print("  - Port: 5000")
    print("  - Debug: True")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
