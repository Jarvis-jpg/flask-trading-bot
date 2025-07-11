
from flask import Flask, request, jsonify
from trade_logic import AdaptiveTradeLogic
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Example: You'll later fetch this from live API or TradingView webhook
    pair = data.get("pair")
    signal = data.get("signal")
    price = float(data.get("price"))
    time = data.get("time")

    # Dummy data for testing - replace with live candle fetching
    df = pd.read_csv("test_candles.csv")  # You must provide this or fetch live

    logic = AdaptiveTradeLogic(df)
    model_signal = logic.get_signal()

    if model_signal == signal:
        atr = 0.0012  # Replace with dynamic ATR calculation
        sl, tp = logic.stop_loss_take_profit(price, signal, atr)
        return jsonify({
            "status": "Trade Executed",
            "pair": pair,
            "signal": signal,
            "price": price,
            "SL": sl,
            "TP": tp
        }), 200
    else:
        return jsonify({"status": "Signal filtered out"}), 200

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
