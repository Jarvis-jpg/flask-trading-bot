from flask import request, jsonify
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
        data = request.get_json(force=True)

        # Extract data fields
        ticker = data.get('ticker')
        side = data.get('side')
        price = data.get('price')
        strategy = data.get('strategy')
        time = data.get('time')

        # Log it for debug
        print(f"Webhook received:\n"
              f"Ticker: {ticker}\nSide: {side}\nPrice: {price}\n"
              f"Strategy: {strategy}\nTime: {time}")

        return jsonify({"status": "success", "message": "Webhook received"}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
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


