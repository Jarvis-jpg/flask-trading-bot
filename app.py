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
            # Extract required fields from data
            result = {
                'pair': data['pair'],
                'action': data['action'],
                'entry': float(data['entry']),
                'stop_loss': float(data['stop_loss']),
                'take_profit': float(data['take_profit']),
                'confidence': float(data['confidence']),
                'strategy': data['strategy'],
                'timestamp': data['timestamp'],
                'result': 'pending',  # Initial trade result
                'profit': 0.0  # Initial profit
            }
            
            # Execute trade and log it
            trade_result = execute_trade(data)
            log_trade(**result)  # Unpack result dictionary as keyword arguments
            analyze_trade(trade_result)
            
            return jsonify({'status': 'Trade executed', 'details': trade_result}), 200
            
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    print("\n🚀 Starting Jarvis Trading Bot...")
    print("📡 Routes configured:")
    print("  - GET  /")
    print("  - POST /webhook")
    app.run(host='127.0.0.1', port=5000, debug=True)