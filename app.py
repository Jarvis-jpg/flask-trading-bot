from flask import Flask, request, jsonify
from jarvis_ui import jarvis_ui
from learner import analyze_and_learn
from trade_logic import process_trade
from ai_learning import train_ai

app = Flask(__name__)
app.register_blueprint(jarvis_ui, url_prefix="/")

if __name__ == "__main__":
    app.run()


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.is_json:
            trade_data = request.get_json()
        else:
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400

        # Extract each field safely
        ticker = trade_data.get("ticker")
        side = trade_data.get("side")
        price = trade_data.get("price")
        strategy = trade_data.get("strategy")
        time = trade_data.get("time")

        print("Webhook received:")
        print("Ticker:", ticker)
        print("Side:", side)
        print("Price:", price)
        print("Strategy:", strategy)
        print("Time:", time)

        return jsonify({"status": "success", "message": "Trade received"}), 200

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


