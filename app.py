from learner import analyze_and_learn
from trade_logic import process_trade
from ai_learning import train_ai
from flask import Flask
from jarvis_ui import jarvis_ui

app = Flask(__name__)
app.register_blueprint(jarvis_ui, url_prefix="/")

if __name__ == "__main__":
    app.run()



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


