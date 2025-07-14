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

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("Received webhook data:", data)
        process_trade(data)
        return jsonify({"message": "Trade processed", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"ERROR: {e}", "status": "error"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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



