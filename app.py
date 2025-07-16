from flask import Flask, request, jsonify
from trade_logic import process_trade

app = Flask(__name__)

@app.route('/')
def home():
return "✅ Quant Trading Bot is Live"

@app.route('/webhook', methods=['POST'])
def webhook():
data = request.get_json()
if not data:
return jsonify({'error': 'Missing JSON data'}), 400

try:
result = process_trade(data)
return jsonify({'message': result}), 200
except Exception as e:
print(f"ERROR in webhook: {e}")
return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
app.run(debug=True)
