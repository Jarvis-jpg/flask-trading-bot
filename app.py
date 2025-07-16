from flask import Flask, request, jsonify
from trade_logic import execute_trade
from journal_logger import log_trade
from ai_predict import analyze_trade

app = Flask(__name__)

@app.route('/')
def home():
return "✅ Quant Trading Bot is Live"

@app.route('/webhook', methods=['POST'])
def webhook():
if request.method == 'POST':
data = request.get_json()

if not data:
return jsonify({'error': 'No data received'}), 400

try:
result = execute_trade(data)
log_trade(result)
analyze_trade(result)
return jsonify({'status': 'Trade executed', 'details': result}), 200
except Exception as e:
return jsonify({'error': str(e)}), 500
else:
return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
app.run(debug=True)
