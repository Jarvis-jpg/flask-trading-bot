import pandas as pd
from flask import Flask, request, jsonify
from jarvis_ui import jarvis_ui
from learner import analyze_and_learn
from trade_logic import process_trade
from ai_learning import train_ai
from utils.journal_logger import log_trade

app = Flask(__name__)
app.register_blueprint(jarvis_ui, url_prefix="/")

if __name__ == "__main__":
    app.run()

@app.route('/')
def home():
    return "Quant AI Trading System is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
    try:
        process_trade(data)
        return jsonify({"message": "Trade processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
@app.route("/learn", methods=["GET"])
def learn():
    result = train_ai()
    return jsonify({"status": "ok", "message": result})
@app.route('/ai/train', methods=['GET'])
def trigger_ai_training():
    from ai.train import run_ai_training
    result = run_ai_training()
    return jsonify({"message": result, "status": "success"})



