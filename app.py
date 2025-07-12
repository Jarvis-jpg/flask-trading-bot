from flask import Flask, request, jsonify
from trade_logic import process_trade
from dashboard import dashboard_app
  # Make sure dashboard.py exists

app = Flask(__name__)
app.register_blueprint(dashboard_app, url_prefix="/", name="dashboard_unique")



@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = request.get_json()
            result = process_trade(data)
            return jsonify({"status": "success", "details": result}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "Invalid method"}), 400


if __name__ == "__main__":
    app.run(debug=True)
@app.route('/', methods=['GET'])
def index():
    return "Trading Bot is Live!"
app.register_blueprint(dashboard_app, url_prefix="/")
