from flask import Flask, request, jsonify
from trade_logic import process_trade

app = Flask(__name__)

@app.route('/')
def home():
return "✅ Quant Trading Bot is Live"

@app.route('/webhook', methods=['POST'])
def webhook():
data = request.json
if not data:
return jsonify({"error": "No data received"}), 400
try:
result = process_trade(data)
return jsonify(result)
except Exception as e:
return jsonify({"error": str(e)}), 500

try:
response = process_trade(data)
return jsonify({"message": "✅ Trade processed", "result": response})
except Exception as e:
print("ERROR in process_trade:", str(e))
return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
app.run(debug=True)
