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
        data = request.get_json()

        ticker = data.get("ticker")
        side = data.get("side")
        price = data.get("price")
        strategy = data.get("strategy")
        time = data.get("time")

        print(f"Webhook received:\nTicker: {ticker}\nSide: {side}\nPrice: {price}\nStrategy: {strategy}\nTime: {time}")

        # Save trade to CSV
        trade = {
            "time": time,
            "ticker": ticker,
            "side": side,
            "price": price,
            "strategy": strategy
        }

        df = pd.DataFrame([trade])
        if not os.path.exists("trades.csv"):
            df.to_csv("trades.csv", index=False)
        else:
            df.to_csv("trades.csv", mode='a', header=False, index=False)
       # TEMPORARY: Trigger AI learning module after trade is received
        import subprocess
        subprocess.Popen(["python", "ai_learning.py"])

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(e)
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


