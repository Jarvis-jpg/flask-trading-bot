import logging
import json
from flask import Flask, request, jsonify
from oanda_client import OandaClient
from datetime import datetime
import numpy as np
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Flask app
app = Flask(__name__)

# Initialize OANDA client
oanda = OandaClient(environment="live")

def calculate_position_size(price, stop_loss, account_balance=25000, risk_percent=4.0):
    """Calculate position size based on risk parameters"""
    risk_amount = account_balance * (risk_percent / 100)
    price_difference = abs(float(price) - float(stop_loss))
    if price_difference == 0:
        return 0
    position_size = round(risk_amount / price_difference)
    return position_size

@app.route("/")
def home():
    return "JARVIS Trading System - Online"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Received webhook data: {json.dumps(data, indent=2)}")

        required_fields = ["symbol", "action", "price", "strategy", "stop_loss", "take_profit"]
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        # Get current price from OANDA
        current_price = oanda.get_price(data["symbol"])
        if not current_price:
            logging.warning(f"No live price available for {data["symbol"]}, using simulation")
            current_price = {
                "bid": float(data["price"]) - 0.0002,
                "ask": float(data["price"]) + 0.0002
            }

        # Calculate position size
        position_size = calculate_position_size(
            data["price"],
            data["stop_loss"]
        )

        # Prepare trade data
        oanda_trade_data = {
            "symbol": data["symbol"],
            "units": position_size if data["action"] == "BUY" else -position_size,
            "stop_loss": data["stop_loss"],
            "take_profit": data["take_profit"]
        }

        logging.info(f"Prepared OANDA trade: {data["action"]} {abs(position_size)} units, SL: {data["stop_loss"]}, TP: {data["take_profit"]}")

        try:
            # Place trade with OANDA
            trade_result = oanda.place_trade(oanda_trade_data)

            if isinstance(trade_result, dict):
                if "error" in trade_result:
                    logging.error(f"Trade placement failed: {trade_result["error"]}")
                    return jsonify(trade_result), 500
                logging.info(f"Trade placed successfully: {json.dumps(trade_result, indent=2)}")
                return jsonify(trade_result), 200
            else:
                logging.error("Invalid trade result format")
                return jsonify({"error": "Invalid trade result format"}), 500

        except Exception as trade_error:
            error_msg = f"Error placing trade: {str(trade_error)}"
            logging.error(error_msg)
            return jsonify({"error": error_msg, "traceback": traceback.format_exc()}), 500

    except Exception as e:
        error_msg = f"Error processing webhook: {str(e)}"
        logging.error(error_msg)
        return jsonify({"error": error_msg, "traceback": traceback.format_exc()}), 500

if __name__ == "__main__":
    print("\nOANDA Configuration:")
    print(f"  - Account: {oanda.account_id}")
    print(f"  - Mode: {oanda.environment.upper()}")
    print(f"  - API URL: {oanda.api_url}/v3")

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
