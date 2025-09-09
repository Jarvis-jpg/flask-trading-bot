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

        # Handle both JARVIS Live format and TradingView SevenSYS format
        if 'pair' in data and 'action' in data and 'entry' in data:
            # JARVIS Live Pine Script format
            symbol = data.get("pair", "").upper()
            action = data.get("action", "").lower()  
            price = data.get("entry", 0)
            stop_loss = data.get("stop_loss", 0)
            take_profit = data.get("take_profit", 0)
            logging.info(f"JARVIS Live format detected: {symbol} {action}")
        else:
            # TradingView SevenSYS format (fallback)
            symbol = data.get("ticker") or data.get("symbol", "")
            action = data.get("strategy.order.action") or data.get("action", "")
            price = data.get("close") or data.get("price", 0)
            stop_loss = data.get("stop_loss", 0)
            take_profit = data.get("take_profit", 0)
            logging.info(f"TradingView SevenSYS format detected: {symbol} {action}")
        
        if not all([symbol, action, price, stop_loss, take_profit]):
            missing = [k for k, v in {"symbol": symbol, "action": action, "price": price, "stop_loss": stop_loss, "take_profit": take_profit}.items() if not v]
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        # Log SevenSYS TP/SL values for analysis
        price_float = float(price)
        stop_loss_float = float(stop_loss) 
        take_profit_float = float(take_profit)
        
        logging.info(f"SevenSYS Signal Analysis:")
        logging.info(f"  Action: {action}")
        logging.info(f"  Entry (close): {price_float}")
        logging.info(f"  Stop Loss: {stop_loss_float}")
        logging.info(f"  Take Profit: {take_profit_float}")
        
        # Calculate distances for validation
        sl_distance = abs(stop_loss_float - price_float)
        tp_distance = abs(take_profit_float - price_float)
        tp_sl_ratio = tp_distance / sl_distance if sl_distance > 0 else 0
        
        logging.info(f"  SL Distance: {sl_distance:.5f} ({sl_distance * 10000:.1f} pips)")
        logging.info(f"  TP Distance: {tp_distance:.5f} ({tp_distance * 10000:.1f} pips)")
        logging.info(f"  Risk/Reward: 1:{tp_sl_ratio:.2f}")
        
        # Warning for extremely large TP/SL distances (but don't reject)
        if sl_distance * 10000 > 200:  # More than 200 pips
            logging.warning(f"Large stop loss: {sl_distance * 10000:.1f} pips - check SevenSYS settings")
        if tp_distance * 10000 > 800:  # More than 800 pips  
            logging.warning(f"Large take profit: {tp_distance * 10000:.1f} pips - check SevenSYS settings")

        # Calculate position size (conservative for small account)
        position_size = calculate_position_size(price, stop_loss, account_balance=45.0, risk_percent=2.0)
        units = position_size if action.lower() == "buy" else -position_size
        
        # Convert symbol to OANDA format (EURUSD -> EUR_USD)
        oanda_symbol = symbol
        if len(symbol) == 6 and '_' not in symbol:
            # Convert EURUSD to EUR_USD
            oanda_symbol = symbol[:3] + '_' + symbol[3:]
        
        trade_data = {
            "symbol": oanda_symbol,
            "units": units,
            "close_price": price_float,  # Original SevenSYS close price
            "stop_loss": round(stop_loss_float, 5),  # Round to 5 decimal places for OANDA
            "take_profit": round(take_profit_float, 5)  # Round to 5 decimal places for OANDA
        }

        logging.info(f"Placing trade: {action} {abs(units)} units of {symbol} -> {oanda_symbol}")
        
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
