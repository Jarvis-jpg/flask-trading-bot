from dashboard import dashboard_app
from learner import analyze_and_learn
from flask import Flask, request, jsonify
from trade_logic import process_trade
from ai_learning import train_ai


app = Flask(__name__)
app.register_blueprint(dashboard_app, url_prefix="/")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        result = process_trade(data)
        return jsonify({"status": "success", "details": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/train", methods=["POST"])
def trigger_training():
    try:
        result = train_ai()
        return jsonify({"status": "training complete", "details": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
@app.route("/learn", methods=["GET"])
def learn():
    result = train_ai()
    return jsonify({"status": "ok", "message": result})
app.register_blueprint(dashboard_app, url_prefix="/")
