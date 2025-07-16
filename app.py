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
return "✅ Quant Trading Bot is Live"

@app.route('/webhook', methods=['POST'])
def webhook():
try:
data = request.get_json()
print("Received webhook data:", data)

result = process_trade(data)
return jsonify({"status": "success", "result": result})
except Exception as e:
print("ERROR in process_trade:", str(e))
return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
app.run(debug=True)

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



