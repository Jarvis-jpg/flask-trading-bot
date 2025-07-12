from dashboard import dashboard
from flask import Flask, request, jsonify
from trade_logic import AdaptiveTradeLogic  # Must exist

app = Flask(__name__)app.register_blueprint(dashboard, url_prefix="/")


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    try:
        trade_result = AdaptiveTradeLogic.execute_trade(data)
        return jsonify({"status": "success", "details": trade_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
app.register_blueprint(dashboard_app, url_prefix="/")
