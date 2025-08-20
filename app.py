import logging
import json
from flask import Flask, request, jsonify
from oanda_client import OandaClient     
from datetime import datetime
import numpy as np
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

def calculate_position_size(price, stop_loss, account_balance=50, risk_percent=4.0):
    try:
        risk_amount = account_balance * (risk_percent / 100)
        price_difference = abs(float(price) - float(stop_loss))
        if price_difference == 0:
            return 100
        position_size = round(risk_amount / price_difference)
        # Cap position size for demo/small accounts  
        return max(1000, min(position_size, 5000))
    except Exception as e:
        logging.error(f"Error calculating position size: {e}")
        return 100

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

        # Handle both custom format and PineScript default format
        if "ticker" in data:
            # PineScript default format
            symbol = data.get("ticker", "EURUSD")
            action = data.get("strategy.order.action", "buy")
            price = float(data.get("close", 1.0850))
            strategy = data.get("strategy", "PineScript")
            
            # Calculate reasonable stop loss and take profit based on price
            if action.lower() == "buy":
                stop_loss = round(price * 0.995, 5)   # 0.5% below entry, 5 decimal places
                take_profit = round(price * 1.005, 5)  # 0.5% above entry, 5 decimal places
            else:  # sell
                stop_loss = round(price * 1.005, 5)   # 0.5% above entry, 5 decimal places
                take_profit = round(price * 0.995, 5)  # 0.5% below entry, 5 decimal places
        else:
            # Custom format
            required_fields = ["symbol", "action", "price", "strategy", "stop_loss", "take_profit"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
            
            symbol = data["symbol"]
            action = data["action"]
            price = float(data["price"])
            strategy = data["strategy"]
            stop_loss = float(data["stop_loss"])
            take_profit = float(data["take_profit"])

        position_size = calculate_position_size(price, stop_loss)
        units = position_size if action.upper() == "BUY" else -position_size

        trade_data = {
            "symbol": symbol,
            "units": units,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

        logging.info(f"Placing trade: {action} {abs(units)} units of {symbol}")

        try:
            trade_result = oanda.place_trade(trade_data)
            logging.info("Trade placed successfully")
            return jsonify({
                "status": "success",
                "message": "Trade placed successfully",
                "trade_data": trade_result
            }), 200
        except Exception as trade_error:
            error_msg = str(trade_error)
            logging.error(f"Trade execution failed: {error_msg}")
            return jsonify({
                "status": "error", 
                "message": f"Trade execution failed: {error_msg}"
            }), 400

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
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

    print("\nStarting server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
