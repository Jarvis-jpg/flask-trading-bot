from flask import Flask, request, jsonify
from trade_logic import execute_trade
from utils.journal_logger import log_trade
from ai_predict import analyze_trade

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Jarvis Dashboard</h1>"

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
    
    return jsonify({'error': 'Invalid request method'}), 405

# Fixed syntax error in app.run()
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)