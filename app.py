from ai_learning import train_ai
from learner import analyze_and_learn
from flask import Flask, request, jsonify
from trade_logic import process_trade
from dashboard import jarvis


app = Flask(__name__)
app.register_blueprint(jarvis), url_prefix="/")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        trade_data = request.get_json()
        result = process_trade(trade_data)
        return jsonify({"status": "success", "details": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/train", methods=["POST"])
def train():
    from ai_learning import train_ai
    try:
        train_ai()
        return jsonify({"status": "training complete"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
@app.route("/learn", methods=["GET"])
def learn():
    result = train_ai()
    return jsonify({"status": "ok", "message": result})
app.register_blueprint(jarvis), url_prefix="/")

