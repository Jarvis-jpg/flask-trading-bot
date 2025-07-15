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
        data = request.get_json()
        print("Received webhook data:", data)

        # Patch: Convert TradingView fields to expected fields if needed
        if 'ticker' in data and 'side' in data and 'price' in data:
            data['pair'] = data.pop('ticker')
            data['action'] = data.pop('side')
            data['entry'] = data.pop('price')
            data['timestamp'] = data.pop('time')
            # Add default SL/TP/confidence if missing
            entry = float(data['entry'])
            if data['action'] == 'buy':
                data['stop_loss'] = round(entry - 0.0020, 5)
                data['take_profit'] = round(entry + 0.0040, 5)
            else:
                data['stop_loss'] = round(entry + 0.0020, 5)
                data['take_profit'] = round(entry - 0.0040, 5)
            data['confidence'] = 0.75  # Default if not sent
            print("✅ Translated TradingView alert to internal format.")

        process_trade(data)
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print("ERROR in webhook:", e)
        return jsonify({'error': str(e)}), 400


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



